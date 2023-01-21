from urllib.parse import urlparse, urljoin
import subprocess
from optparse import OptionParser
import threading
from colorama import Fore
import os
available_modes = ['quick','full','default','parameter','custom'] #For reference

parser = OptionParser()
parser.add_option('-d',dest='domain',help='Enter a domain to scan')
parser.add_option('-m',dest='mode',help='Enter the Scanning mode(quick,default,full, custom,parameter or extension)')
parser.add_option('-f',dest='filename',help='Custom file')
parser.add_option('-t',dest='threads',help='Enter the speed of this program.')
val, arg = parser.parse_args()

if val.mode not in available_modes:
	print(Fore.RED + '[+] Please check the domain name or the given mode carefully')
	quit()
print(Fore.GREEN + '''
  ______ _______ _______  _______ _     _ _______  _____  _______ _______ _______  _____   ______
 |  ____ |______    |     |_____| |     |    |    |     | |  |  | |_____|    |    |     | |_____/
 |_____| |______    |     |     | |_____|    |    |_____| |  |  | |     |    |    |_____| |    \_
				#Automate Arjun With Speed & Efficiency
					#By Faiyaz Ahmad
					@BePracticalTech
''')


class Automation:

	def __init__(self,domain,mode='default'):
		#array = ['https://google.com','https://bing.com']
		#print(self.threads(1,array))
		self.total_threads = []
		self.domain = domain
		self.mode = mode;self.ext = ['jsp','aspx','asp','php']
		if val.filename:
			if val.mode != 'custom':
				print(Fore.RED + 'Error! Please check the mode used')
				quit()
			with open(val.filename,'r') as data:
				links = data.read().split()
				data.close()
			i = 0
			for link in links:
				parsed_url = urlparse(link)
				new_link = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'
				links[i] = new_link
				i += 1
			if val.threads:
				if int(val.threads) <= 10:
					links = self.threads(int(val.threads),links)
					index = 0
					#print(links)
					for link in links:
						#print(link)
						self.total_threads.append(threading.Thread(target=self.scanner,args=(link,)))
						#self.total_threads[index].start()
						#index += 1
						#print(1)
					#print(len(self.total_threads))
					for thread in self.total_threads:
						#print('Thread Started')
						thread.start()
			else:
				#print(links)
				self.scanner(links)
		else:
			data = self.domain_scanner(self.domain)
			parsed_data = self.parser(data,self.mode)
			if val.threads:
				val.threads = int(val.threads)
				if int(val.threads) <= 10:
					parsed_data = self.threads(int(val.threads),parsed_data)
					#print(parsed_data)
					for data in parsed_data:
						self.total_threads.append(threading.Thread(target=self.scanner,args=(data,)))
					for thread in self.total_threads:
						thread.start()
			else:
				self.scanner(parsed_data)

	def threads(self,value,array):
		final_list = []
		temp_list = []
		num = 0
		total_len =  len(array)
		while num <= total_len:
			if len(temp_list) == value:
				#print('yes')
				final_list.append(temp_list)
				temp_list = []
				continue

			else:
				if len(array):
					temp_list.append(array.pop(0))
			#print(f'Number: {num}  Array: {temp_list}')
			num += 1
		else:
			#print(array)
			if temp_list:
				final_list.append(temp_list)
			return final_list

	def domain_scanner(self,domain): #Passive Domain Scanner

		final_list = []
		self.domain = domain
		print(Fore.GREEN + f'[+] Getting Links via GAU (Output filename: {self.domain}_gau.txt)')
		subprocess.call(f'echo {self.domain} | gau > {self.domain}_gau.txt',shell=True)
		with open(f'{self.domain}_gau.txt','r') as file:
			links = file.read().split()
			file.close()
		print(Fore.BLUE + f'[+] {len(links)} Links Found')
		while links:
			dic = {'url':links[0],'isExtension':False,'haveParameter':False,'normalLink':False}
			#dic['link'] = links[i]
			parsed_url = urlparse(links[0])
			try:
				if parsed_url.path.split('.')[1] in self.ext: #Whitelisting extension
					dic['isExtension'] = True
					#dic['url'] = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'
			except:
				if parsed_url.query:
					dic['haveParameter'] = True
					#dic['url'] = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'
				else:
					dic['normalLink'] = True
			final_list.append(dic)
			links.pop(0)
		return final_list

	def parser(self,array,mode):
		data = []
		while array:
			if mode == 'default':
				if array[0]['haveParameter'] or array[0]['isExtension']: #Parameter with and without Extension
					data.append(array[0]['url'])
			elif mode == 'full': #Every Single Link
				data.append(array[0]['url'])
			elif mode == 'quick': # Parameters with extension
				if array[0]['isExtension']:
					urlparsed = urlparse(array[0]['url'])
					data.append(f'{urlparsed.scheme}://{urlparsed.netloc}{urlparsed.path}')
			elif mode == 'parameter': #Parameter without extension
				if array[0]['haveParameter']:
					data.append(array[0]['url'])
			elif mode == 'custom': #Custom File
				pass
			array.pop(0)
		print(Fore.BLUE + '[+] {} Links filtered'.format(len(data)))
		return list(set(data))
	def scanner(self,array):
		#print(array)
		for link in array:
			print(Fore.BLUE + f'[+] Scanning {link}')
			subprocess.check_output(f"arjun -u {link} -m GET >> {link.split('/')[2]}.txt",shell=True)
			with open(f"{link.split('/')[2]}.txt",'a') as data:
				data.write(f'[+] Url: {link}\n')
				data.write('-----------------------------------------------\n')
			print(Fore.GREEN + f'[+] {link} Scanned Successfully')
		return None

if __name__ == "__main__":

	Automation(val.domain,val.mode)
	#data = a.domain_scanner()
	#parsed_data = a.parser(data,'quick')
	#print(parsed_data)

