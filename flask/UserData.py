#!/usr/bin/env python
import re, os, sys, time, shutil, numpy, cgi, cgitb
from UserInfo import *


##CReates Database for User Data.
class UserData:
	""" 
	User Data acts as a buffer for user information retrieval from the database as well as working with local data
	"""
	def __init__ (self):
		"""
		Intializes User Data object

		:param self: Object itself
		:type self: self
		:param a: Database ID
		:type a: int
		:param b: User ID
		:type b: User ID generated
		:param c: Gambler project "titleid" or project folder name
		:type c: str
		:param d: User first name 
		:type d: str
		:param e: User last name
		:type e: str
		:param f: User age
		:type f: int
		:param g: Hispanic/Latino designation
		:type g: int/bool
		:param h: User's gender
		:type h: str		
		:param i: User's race
		:type i: str			
		:param j: First Health State Visual Analog Scale utility
		:type j: float
		:param k: Second Health State Visual Analog Scale utility
		:type k: float
		:param l: Third Health State Visual Analog Scale utility
		:type l: float
		:param m: Fourth Health State Visual Analog Scale utility
		:type m: float
		:param n: Fifth Health State Visual Analog Scale utility
		:type n: float
		:param o: Sixth Health State Visual Analog Scale utility
		:type o: float
		:param p: Seventh Health State Visual Analog Scale utility
		:type p: float
		:param q: Eigtht Health State Visual Analog Scale utility
		:type q: float		
		:param r: First Health State Time Trade off utility
		:type r: float
		:param s: Second Health State Time Trade off utility
		:type s: float
		:param t: Third Health State Time Trade off utility
		:type t: float
		:param u: Fourth Health State Time Trade off utility
		:type u: float
		:param v: Fifth Health State Time Trade off utility
		:type v: float
		:param w: Sixth Health State Time Trade off utility
		:type w: float
		:param x: Seventh Health State Time Trade off utility
		:type x: float
		:param y: Eigtht Health State Time Trade off utility
		:type y: float	
		:param z: First Health State Standard Gamble utility
		:type z: float
		:param aa: Second Health State Standard Gamble utility
		:type aa: float
		:param ab: Third Health State Standard Gamble utility
		:type ab: float
		:param ac: Fourth Health State Standard Gamble utility
		:type ac: float
		:param ad: Fifth Health State Standard Gamble utility
		:type ad: float
		:param ae: Sixth Health State Standard Gamble utility
		:type ae: float
		:param af: Seventh Health State Standard Gamble utility
		:type af: float
		:param ag: Eigtht Health State Standard Gamble utility
		:type ag: float	
		:param ah: First Health State Ordinal Ranking 
		:type ah: float
		:param ai: Second Health State Ordinal Ranking 
		:type ai: float
		:param aj: Third Health State Ordinal Ranking 
		:type aj: float
		:param ak: Fourth Health State Ordinal Ranking 
		:type ak: float
		:param al: Fifth Health State Ordinal Ranking 
		:type al: float
		:param am: Sixth Health State Ordinal Ranking 
		:type am: float
		:param an: Seventh Health State Ordinal Ranking 
		:type an: float
		:param ao: Eigtht Health State Ordinal Ranking 
		:type ao: float	
		"""	

		self.uid= 0 #uniqe ID
		self.userid ="" #UserID
		self.titleid="" #GamblerProject they used
		self.firstname =""
		self.lastname =""
		self.age = 0
		self.hld = 0 #HispanicLatino Deisgnator
		self.gender =""
		self.race =""
		self.finalconditionIntensityOne =0                   
		self.finalconditionIntensityTwo =0                   
		self.finalconditionIntensityThree =0                 
		self.finalconditionIntensityFour =0                  
		self.finalconditionIntensityFive =0     
		self.finalconditionIntensitySix =0   
		self.finalconditionIntensitySeven =0   
		self.finalconditionIntensityEight =0             
		self.finalconditionTimeTOne    =0                   
		self.finalconditionTimeTTwo    =0                   
		self.finalconditionTimeTThree  =0                   
		self.finalconditionTimeTFour   =0                   
		self.finalconditionTimeTFive   =0    
		self.finalconditionTimeTSix    =0   
		self.finalconditionTimeTSeven   =0   
		self.finalconditionTimeTEight   =0                  
		self.finalconditionGambOne     =0                   
		self.finalconditionGambTwo     =0                   
		self.finalconditionGambThree   =0                   
		self.finalconditionGambFour    =0                   
		self.finalconditionGambFive  =0
		self.finalconditionGambSix  =0
		self.finalconditionGambSeven  =0
		self.finalconditionGambEight  =0
		self.finalconditionOrderOne   =""          
		self.finalconditionOrderTwo   =""     
		self.finalconditionOrderThree =""        
		self.finalconditionOrderFour   =""        
		self.finalconditionOrderFive =""
		self.finalconditionOrderSix =""
		self.finalconditionOrderSeven =""
		self.finalconditionOrderEight =""
	
	def dbload(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, ab, ac, ad, ae, af, ag, ah, ai,aj,ak,al, am, an, ao):
		"""
		Loads patient's data into a database

		:param self: Object itself
		:type self: self
		:param a: Database ID
		:type a: int
		:param b: User ID
		:type b: User ID generated
		:param c: Gambler project "titleid" or project folder name
		:type c: str
		:param d: User first name 
		:type d: str
		:param e: User last name
		:type e: str
		:param f: User age
		:type f: int
		:param g: Hispanic/Latino designation
		:type g: int/bool
		:param h: User's gender
		:type h: str		
		:param i: User's race
		:type i: str			
		:param j: First Health State Visual Analog Scale utility
		:type j: float
		:param k: Second Health State Visual Analog Scale utility
		:type k: float
		:param l: Third Health State Visual Analog Scale utility
		:type l: float
		:param m: Fourth Health State Visual Analog Scale utility
		:type m: float
		:param n: Fifth Health State Visual Analog Scale utility
		:type n: float
		:param o: Sixth Health State Visual Analog Scale utility
		:type o: float
		:param p: Seventh Health State Visual Analog Scale utility
		:type p: float
		:param q: Eigtht Health State Visual Analog Scale utility
		:type q: float		
		:param r: First Health State Time Trade off utility
		:type r: float
		:param s: Second Health State Time Trade off utility
		:type s: float
		:param t: Third Health State Time Trade off utility
		:type t: float
		:param u: Fourth Health State Time Trade off utility
		:type u: float
		:param v: Fifth Health State Time Trade off utility
		:type v: float
		:param w: Sixth Health State Time Trade off utility
		:type w: float
		:param x: Seventh Health State Time Trade off utility
		:type x: float
		:param y: Eigtht Health State Time Trade off utility
		:type y: float	
		:param z: First Health State Standard Gamble utility
		:type z: float
		:param aa: Second Health State Standard Gamble utility
		:type aa: float
		:param ab: Third Health State Standard Gamble utility
		:type ab: float
		:param ac: Fourth Health State Standard Gamble utility
		:type ac: float
		:param ad: Fifth Health State Standard Gamble utility
		:type ad: float
		:param ae: Sixth Health State Standard Gamble utility
		:type ae: float
		:param af: Seventh Health State Standard Gamble utility
		:type af: float
		:param ag: Eigtht Health State Standard Gamble utility
		:type ag: float	
		:param ah: First Health State Ordinal Ranking 
		:type ah: float
		:param ai: Second Health State Ordinal Ranking 
		:type ai: float
		:param aj: Third Health State Ordinal Ranking 
		:type aj: float
		:param ak: Fourth Health State Ordinal Ranking 
		:type ak: float
		:param al: Fifth Health State Ordinal Ranking 
		:type al: float
		:param am: Sixth Health State Ordinal Ranking 
		:type am: float
		:param an: Seventh Health State Ordinal Ranking 
		:type an: float
		:param ao: Eigtht Health State Ordinal Ranking 
		:type ao: float	
		"""	
		self.uid= a
		self.userid =b
		self.titleid=c
		self.firstname =d
		self.lastname =e
		self.age = f
		self.hld = g
		self.gender =h
		self.race =i
		self.finalconditionIntensityOne =j                  
		self.finalconditionIntensityTwo =k                  
		self.finalconditionIntensityThree =l                 
		self.finalconditionIntensityFour =m                
		self.finalconditionIntensityFive =n     
		self.finalconditionIntensitySix =o 
		self.finalconditionIntensitySeven =p   
		self.finalconditionIntensityEight =q             
		self.finalconditionTimeTOne    =r                   
		self.finalconditionTimeTTwo    =s                   
		self.finalconditionTimeTThree  =t                   
		self.finalconditionTimeTFour   =u                   
		self.finalconditionTimeTFive   =v    
		self.finalconditionTimeTSix    =w   
		self.finalconditionTimeTSeven   =x   
		self.finalconditionTimeTEight   =y                  
		self.finalconditionGambOne     =z                 
		self.finalconditionGambTwo     =aa                   
		self.finalconditionGambThree   =ab                   
		self.finalconditionGambFour    =ac                  
		self.finalconditionGambFive  =ad
		self.finalconditionGambSix  =ae
		self.finalconditionGambSeven  =af
		self.finalconditionGambEight  =ag
		self.finalconditionOrderOne   =ah          
		self.finalconditionOrderTwo   =ai     
		self.finalconditionOrderThree =aj  #Heh             
		self.finalconditionOrderFour   =ak 
		self.finalconditionOrderFive =al
		self.finalconditionOrderSix =am
		self.finalconditionOrderSeven =an
		self.finalconditionOrderEight =ao
		
	##Save Demographic data
	def demosave(self, a, b, c, d, e, f, g, h, i):
		"""
		Saves demographic data and patient info as application local data
		
		:param self: Object itself
		:type self: self
		:param a: Database ID
		:type a: int
		:param b: User ID
		:type b: User ID generated
		:param c: Gambler project "titleid" or project folder name
		:type c: str
		:param d: User first name 
		:type d: str
		:param e: User last name
		:type e: str
		:param f: User age
		:type f: int
		:param g: Hispanic/Latino designation
		:type g: int/bool
		:param h: User's gender
		:type h: str		
		:param i: User's race
		:type i: str			
		"""	
		self.uid = a
		self.userid =b
		self.titleid=c
		self.firstname =d
		self.lastname =e
		self.age = f
		self.hld = g
		self.gender =h
		self.race =i
##Save intensity final results
	def intensave(self,j, k, l, m, n, o, p, q ):
		"""
		Saves Visual Analog Scale as application local data	
		
		:param self: Object itself
		:type self: self
		:param j: First Health State Visual Analog Scale utility
		:type j: float
		:param k: Second Health State Visual Analog Scale utility
		:type k: float
		:param l: Third Health State Visual Analog Scale utility
		:type l: float
		:param m: Fourth Health State Visual Analog Scale utility
		:type m: float
		:param n: Fifth Health State Visual Analog Scale utility
		:type n: float
		:param o: Sixth Health State Visual Analog Scale utility
		:type o: float
		:param p: Seventh Health State Visual Analog Scale utility
		:type p: float
		:param q: Eigtht Health State Visual Analog Scale utility
		:type q: float		
		
		"""
		self.finalconditionIntensityOne =j                  
		self.finalconditionIntensityTwo =k                  
		self.finalconditionIntensityThree =l                 
		self.finalconditionIntensityFour =m                
		self.finalconditionIntensityFive =n     
		self.finalconditionIntensitySix =o 
		self.finalconditionIntensitySeven =p   
		self.finalconditionIntensityEight =q  
##Save Time trade final results
	def timetsave(self,r, s, t, u, v, w, x, y):
		"""
		Saves Time Trade off as application local data	
		
		:param self: Object itself
		:type self: self
		:param r: First Health State Time Trade off utility
		:type r: float
		:param s: Second Health State Time Trade off utility
		:type s: float
		:param t: Third Health State Time Trade off utility
		:type t: float
		:param u: Fourth Health State Time Trade off utility
		:type u: float
		:param v: Fifth Health State Time Trade off utility
		:type v: float
		:param w: Sixth Health State Time Trade off utility
		:type w: float
		:param x: Seventh Health State Time Trade off utility
		:type x: float
		:param y: Eigtht Health State Time Trade off utility
		:type y: float		
		
		""" 
		self.finalconditionTimeTOne    =r                   
		self.finalconditionTimeTTwo    =s                   
		self.finalconditionTimeTThree  =t                   
		self.finalconditionTimeTFour   =u                   
		self.finalconditionTimeTFive   =v    
		self.finalconditionTimeTSix    =w   
		self.finalconditionTimeTSeven   =x   
		self.finalconditionTimeTEight   =y   
##Save GAmbler final results
	def gambsave(self, z, aa, ab, ac, ad, ae, af, ag):
		"""
		Saves Standard Gamble as application local data	
		
		:param self: Object itself
		:type self: self
		:param z: First Health State Standard Gamble utility
		:type z: float
		:param aa: Second Health State Standard Gamble utility
		:type aa: float
		:param ab: Third Health State Standard Gamble utility
		:type ab: float
		:param ac: Fourth Health State Standard Gamble utility
		:type ac: float
		:param ad: Fifth Health State Standard Gamble utility
		:type ad: float
		:param ae: Sixth Health State Standard Gamble utility
		:type ae: float
		:param af: Seventh Health State Standard Gamble utility
		:type af: float
		:param ag: Eigtht Health State Standard Gamble utility
		:type ag: float		
		
		"""
		self.finalconditionGambOne     =z                 
		self.finalconditionGambTwo     =aa                   
		self.finalconditionGambThree   =ab                   
		self.finalconditionGambFour    =ac                  
		self.finalconditionGambFive  =ad
		self.finalconditionGambSix  =ae
		self.finalconditionGambSeven  =af
		self.finalconditionGambEight  =ag
	##Save order final results
	def ordersave(self, ah, ai,aj,ak,al, am, an, ao):
		"""
		Saves Ordinal Ranking as application local data	
		
		:param self: Object itself
		:type self: self
		:param ah: First Health State Ordinal Ranking 
		:type ah: float
		:param ai: Second Health State Ordinal Ranking 
		:type ai: float
		:param aj: Third Health State Ordinal Ranking 
		:type aj: float
		:param ak: Fourth Health State Ordinal Ranking 
		:type ak: float
		:param al: Fifth Health State Ordinal Ranking 
		:type al: float
		:param am: Sixth Health State Ordinal Ranking 
		:type am: float
		:param an: Seventh Health State Ordinal Ranking 
		:type an: float
		:param ao: Eigtht Health State Ordinal Ranking 
		:type ao: float		
		
		"""
		self.finalconditionOrderOne   =ah          
		self.finalconditionOrderTwo   =ai     
		self.finalconditionOrderThree =aj            
		self.finalconditionOrderFour   =ak 
		self.finalconditionOrderFive =al
		self.finalconditionOrderSix =am
		self.finalconditionOrderSeven =an
		self.finalconditionOrderEight =ao
	def orderdbsave(self, gtid, a,b,c,d, e,f,g,h):
		"""
		Saves Ordinal Ranking into the database for users	
		
		:param self: Object itself
		:type self: self
		:param guid: User ID from the Gambler
		:type guid: str
		:param a: First Health State Ordinal Ranking 
		:type a: float
		:param b: Second Health State Ordinal Ranking 
		:type b: float
		:param c: Third Health State Ordinal Ranking 
		:type c: float
		:param d: Fourth Health State Ordinal Ranking 
		:type d: float
		:param e: Fifth Health State Ordinal Ranking 
		:type e: float
		:param f: Sixth Health State Ordinal Ranking 
		:type f: float
		:param g: Seventh Health State Ordinal Ranking 
		:type g: float
		:param h: Eigtht Health State Ordinal Ranking 
		:type h: float		
		:returns: UserInfo object
		:raises: Peewee error
		
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamUI = UserInfo.update(finalconditionOrderOne=a, finalconditionOrderTwo=b, finalconditionOrderThree=c, finalconditionOrderFour=d, finalconditionOrderFive=e, finalconditionOrderSix=f, finalconditionOrderSeven=g, finalconditionOrderEight=h).where(UserInfo.uid == gtid)
		GamUI.execute()
		db.close()
	def intendbsave(self, gtid, a,b,c,d, e,f,g,h):
		"""
		Saves Visual Analog Scale into the database for users	
		
		:param self: Object itself
		:type self: self
		:param guid: User ID from the Gambler
		:type guid: str
		:param a: First Health State Visual Analog Scale utility
		:type a: float
		:param b: Second Health State Visual Analog Scale utility
		:type b: float
		:param c: Third Health State Visual Analog Scale utility
		:type c: float
		:param d: Fourth Health State Visual Analog Scale utility
		:type d: float
		:param e: Fifth Health State Visual Analog Scale utility
		:type e: float
		:param f: Sixth Health State Visual Analog Scale utility
		:type f: float
		:param g: Seventh Health State Visual Analog Scale utility
		:type g: float
		:param h: Eigtht Health State Visual Analog Scale utility
		:type h: float		
		:returns: UserInfo object
		:raises: Peewee error
		
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamUI = UserInfo.update(finalconditionIntensityOne=a, finalconditionIntensityTwo=b, finalconditionIntensityThree=c, finalconditionIntensityFour=d, finalconditionIntensityFive=e, finalconditionIntensitySix=f, finalconditionIntensitySeven=g, finalconditionIntensityEight=h).where(UserInfo.uid == gtid)
		GamUI.execute()
		db.close()
	def gambdbsave(self, gtid, a,b,c,d, e,f,g,h):
		"""
		Saves Standard Gamble into the database for users	

		:param self: Object itself
		:type self: self
		:param guid: User ID from the Gambler
		:type guid: str
		:param a: First Health State Standard Gamble utility
		:type a: float
		:param b: Second Health State Standard Gamble utility
		:type b: float
		:param c: Third Health State Standard Gamble utility
		:type c: float
		:param d: Fourth Health State Standard Gamble utility
		:type d: float
		:param e: Fifth Health State Standard Gamble utility
		:type e: float
		:param f: Sixth Health State Standard Gamble utility
		:type f: float
		:param g: Seventh Health State Standard Gamble utility
		:type g: float
		:param h: Eigtht Health State Standard Gamble utility
		:type h: float		
		:returns: UserInfo object
		:raises: Peewee error
		
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()       
		GamUI = UserInfo.update(finalconditionGambOne=a, finalconditionGambTwo=b, finalconditionGambThree=c, finalconditionGambFour=d, finalconditionGambFive=e, finalconditionGambSix=f, finalconditionGambSeven=g, finalconditionGambEight=h).where(UserInfo.uid == gtid)
		GamUI.execute()
		db.close()
	def timetdbsave(self, gtid, a,b,c,d, e,f,g,h):
		"""
		Saves Time Trade off into the database for users	

		:param self: Object itself
		:type self: self
		:param guid: User ID from the Gambler
		:type guid: str
		:param a: First Health State Time Trade off utility
		:type a: float
		:param b: Second Health State Time Trade off utility
		:type b: float
		:param c: Third Health State Time Trade off utility
		:type c: float
		:param d: Fourth Health State Time Trade off utility
		:type d: float
		:param e: Fifth Health State Time Trade off utility
		:type e: float
		:param f: Sixth Health State Time Trade off utility
		:type f: float
		:param g: Seventh Health State Time Trade off utility
		:type g: float
		:param h: Eigtht Health State Time Trade off utility
		:type h: float		
		:returns: UserInfo object
		:raises: Peewee error
		
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		GamUI = UserInfo.update(finalconditionTimeTOne=a, finalconditionTimeTTwo=b, finalconditionTimeTThree=c, finalconditionTimeTFour=d, finalconditionTimeTFive=e, finalconditionTimeTSix=f, finalconditionTimeTSeven=g, finalconditionTimeTEight=h).where(UserInfo.uid == gtid)
		GamUI.execute()
		db.close()
	def retrievefinal(self, guid):
		"""
		Retrieve health utility data from a user through a userid, normally done at the end of the assessment
		
		:param self: Object itself
		:type self: self
		:param guid: User ID from the Gambler
		:type guid: str
		:returns: UserInfo object -- information retrieved from query lookup.
		:raises: Peewee error
		
		"""
		if (db.is_closed()==False):
			db.close()
		db.connect()
		try:
			GamUI = UserInfo.get(UserInfo.uid == guid)
		except:
			GamUI = UserInfo.get(UserInfo.userid == guid)
		self.finalconditionIntensityOne = GamUI.finalconditionIntensityOne                
		self.finalconditionIntensityTwo =GamUI.finalconditionIntensityTwo                 
		self.finalconditionIntensityThree =GamUI.finalconditionIntensityThree              
		self.finalconditionIntensityFour =GamUI.finalconditionIntensityFour              
		self.finalconditionIntensityFive =GamUI.finalconditionIntensityFive     
		self.finalconditionIntensitySix =GamUI.finalconditionIntensitySix
		self.finalconditionIntensitySeven =GamUI.finalconditionIntensitySeven
		self.finalconditionIntensityEight =GamUI.finalconditionIntensityEight             
		self.finalconditionTimeTOne    =GamUI.finalconditionTimeTOne                 
		self.finalconditionTimeTTwo    =GamUI.finalconditionTimeTTwo                    
		self.finalconditionTimeTThree  =GamUI.finalconditionTimeTThree                   
		self.finalconditionTimeTFour   =GamUI.finalconditionTimeTFour                   
		self.finalconditionTimeTFive   =GamUI.finalconditionTimeTFive
		self.finalconditionTimeTSix    =GamUI.finalconditionTimeTSix   
		self.finalconditionTimeTSeven   =GamUI.finalconditionTimeTSeven   
		self.finalconditionTimeTEight   =GamUI.finalconditionTimeTEight               
		self.finalconditionGambOne     =GamUI.finalconditionGambOne                  
		self.finalconditionGambTwo     =GamUI.finalconditionGambTwo                   
		self.finalconditionGambThree   =GamUI.finalconditionGambThree                   
		self.finalconditionGambFour    =GamUI.finalconditionGambFour                 
		self.finalconditionGambFive  =GamUI.finalconditionGambFive
		self.finalconditionGambSix  =GamUI.finalconditionGambSix
		self.finalconditionGambSeven  =GamUI.finalconditionGambSeven
		self.finalconditionGambEight  =GamUI.finalconditionGambEight
		self.finalconditionOrderOne   =GamUI.finalconditionOrderOne       
		self.finalconditionOrderTwo   =GamUI.finalconditionOrderTwo    
		self.finalconditionOrderThree =GamUI.finalconditionOrderThree             
		self.finalconditionOrderFour   =GamUI.finalconditionOrderFour
		self.finalconditionOrderFive =GamUI.finalconditionOrderFive
		self.finalconditionOrderSix =GamUI.finalconditionOrderSix
		self.finalconditionOrderSeven =GamUI.finalconditionOrderSeven
		self.finalconditionOrderEight =GamUI.finalconditionOrderEight
		db.close()
