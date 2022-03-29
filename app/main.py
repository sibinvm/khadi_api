
import random, string
from flask import Flask
from flask_restful import Resource,Api,reqparse,abort
from firebase import Firebase 
import werkzeug
import datetime

config = {
	"apiKey": "AIzaSyDQLdsyb8SNTPvRtbw-yA3sduJ0uYeUxNA",
	"authDomain": "infra-falcon-326215.firebaseapp.com",
	"databaseURL": "https://infra-falcon-326215-default-rtdb.firebaseio.com",
	"storageBucket": "infra-falcon-326215.appspot.com",
}

firebase=Firebase(config)
storage=firebase.storage()
db=firebase.database()

app=Flask(__name__)
api=Api(app)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

adminLoginParser = reqparse.RequestParser()
adminLoginParser.add_argument('email', type=str, help='email required', required=True)
adminLoginParser.add_argument('password', type=str, help='password required', required=True)

userRegParser = reqparse.RequestParser()
userRegParser.add_argument('name',type=str,help='name is required',required=True)
userRegParser.add_argument('email',type=str,help='name is required',required=True)
userRegParser.add_argument('mobile',type=str,help='name is required',required=True)
userRegParser.add_argument('password',type=str,help='name is required',required=True)
userRegParser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')

userloginparser = reqparse.RequestParser()
userloginparser.add_argument('email',type=str)
userloginparser.add_argument('mobile',type=str)
userloginparser.add_argument('password',type=str,help='password required',required=True)

productparser = reqparse.RequestParser()
productparser.add_argument('slNo',type=int)
productparser.add_argument('productname',type=str,required=True,help='Name is required')
productparser.add_argument('gender',type=str,required=True,help='gender is required')
productparser.add_argument('photo',type=werkzeug.datastructures.FileStorage, location='files',help='photo is required',action='append')
productparser.add_argument('productPrice',type=int,required=True,help='productRate is required')
productparser.add_argument('offerPrice',type=int)
productparser.add_argument('smallCount')
productparser.add_argument('mediumCount')
productparser.add_argument('lCount')
productparser.add_argument('xlCount')
productparser.add_argument('xxlCount')
productparser.add_argument('offerprice')
productparser.add_argument('color',type=str ,required=True,help='color required')
productparser.add_argument('material',type=str,required=True,help='material required')
productparser.add_argument('pincode',type=str,help='pin required',required=True)
productparser.add_argument('category',type=str,help='category required',required=True)
productparser.add_argument('specifications',type=str,help='specification required',required=True)

userupdateparser = reqparse.RequestParser()
userupdateparser.add_argument('name',type=str)
userupdateparser.add_argument('email',type=str)
userupdateparser.add_argument('mobile',type=str)
userupdateparser.add_argument('password',type=str)
userupdateparser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')

productupdateparser = reqparse.RequestParser()
productupdateparser.add_argument('productname',type=str)
productupdateparser.add_argument('gender',type=str)
productupdateparser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')
productupdateparser.add_argument('productRate',type=int)
productupdateparser.add_argument('smallCount',type=int)
productupdateparser.add_argument('mediumCount',type=int)
productupdateparser.add_argument('lCount',type=int)
productupdateparser.add_argument('xlCount',type=int)
productupdateparser.add_argument('xxlCount',type=int)
productupdateparser.add_argument('offerprice',type=int)
productupdateparser.add_argument('color',type=str)
productupdateparser.add_argument('material',type=str)
productupdateparser.add_argument('category',type=str)
productupdateparser.add_argument('pincode',type=str)

productupdateparser.add_argument('specifications',type=str)

bannerparser = reqparse.RequestParser()
bannerparser.add_argument('banner',type=werkzeug.datastructures.FileStorage, location='files',help='photo is required',action='append')
bannerparser.add_argument('productIds',type=str,action='append')

filterrateparser = reqparse.RequestParser()
filterrateparser.add_argument('catID', type=str, required=True, help='category id required')

filtercolorparser = reqparse.RequestParser()
filtercolorparser.add_argument('catName', type=str, required=True, help='category name required')

cartparser = reqparse.RequestParser()
cartparser.add_argument('slno', type=str, required=True, help='slno required')
cartparser.add_argument('quantity', type=int, required=True, help='quantity required')

cartupdateparser = reqparse.RequestParser()
cartupdateparser.add_argument('quantity', type=int)

wishparser = reqparse.RequestParser()
wishparser.add_argument('slno', type=str, required=True, help='slno required')

class AdminLogin(Resource):
	def post(self):
		args = adminLoginParser.parse_args()
		adminPassword = db.child('userAPI').child('adminPassword').get().val()
		if adminPassword == None:
			adminPassword = 'admin123'
			db.child('userAPI').child('adminPassword').set(adminPassword)
		if 'admin@gmail.com' == args['email'] and adminPassword == args['password']:
			return 'admin'
		else:
			return ''

class UserReg(Resource):
	def post(self):
		args = userRegParser.parse_args()
		# if args['photo']:
		# 	if not allowed_file(args['photo'].filename):
		# 		abort(400, message='unsupported file format')
		userCnt = db.child('userAPI').child('userCnt').get().val()
		if userCnt == None:
			userCnt=0
		userCnt += 1
		db.child('userAPI').child('userCnt').set(userCnt)
		userID = 'USR' + str(100 + userCnt)
		# if args['photo']:
		# 	f = args['photo']
		# 	del args['photo']
		# 	storage.child('userAPI').child('userImage').child(userID).child('pic.jpg').put(f)		
		# else:
		# 	storage.child('userAPI').child('userImage').child(userID).child('pic.jpg').put('static/user.png')
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		# args['imgUrl'] = storage.child('HouseRentalPortal').child('userImage').child(userID).child('pic.jpg').get_url(None)
		userList[userID] = args
		db.child('userAPI').child('userList').set(userList)
		return args

	def get(self):
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		return userList

class UserLogin(Resource):
	def post(self):
		args = userloginparser.parse_args()
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		userID = ''
		for i in userList:
			if userList[i]['email'] == args['email'] or userList[i]['mobile'] == args['mobile']:
				if userList[i]['password'] == args['password']:
					userID = i
		return userID

class bannerAdd(Resource):
	def post(self):
		# db.child('userAPI').child('banners').child('bannerCnt').set(0)
		db.child('userAPI').child('banners').set('')
		args = bannerparser.parse_args()
		banners = args['banner']
		productIds = args['productIds']
		ids = []
		# print(args)
		for idx, val in enumerate(productIds):
			if idx%2==1:
				ids.append(val)
		# print(ids)
		# args['productIds'] = {}
		# args['productIds'] =args['productIds']
		del args['banner']	
		for i in banners:
			if not allowed_file(i.filename):
				abort(400, message='unsupported file format')
		count = 0
		for indx,banner in enumerate(banners):
			# db.child('userAPI').child('banners').child('productIds').child('banner'+str(indx+1)).set(ids[indx])
		# for idx, val in enumerate(productIds):
		# 	if idx%2==1:
			# print(ids[indx],banner)
			count = count+1
			bannerId ='banner'+str(count)
			bannerCnt = db.child('userAPI').child('banners').child('bannerCnt').get().val()
			if bannerCnt == None:
				bannerCnt = 0
			bannerCnt += 1
			db.child('userAPI').child('banners').child('bannerCnt').set(bannerCnt)
			storage.child('userAPI').child('banners').child(bannerId).put(banner)
			bannerUrl = storage.child('userAPI').child('banners').child(bannerId).get_url(None)
			bannerList=db.child('userAPI').child('banners').child('bannerList').get().val()
			if bannerList==None:
				bannerList={}
			bannerList[bannerId]= bannerUrl
			bannerList[bannerId+'product'] = ids[indx]
			print(bannerUrl)
			# db.child('userAPI').child('banners').child('bannerList').child(bannerId)
			db.child('userAPI').child('banners').child('bannerList').set(bannerList)
		return count
	def get(self):
		bannerList=db.child('userAPI').child('banners').child('bannerList').get().val()
		return bannerList

class productReg(Resource):
	def post(self):
		args = productparser.parse_args()
		prodcount = db.child('userAPI').child('prodcount').get().val()
		if prodcount == None:
			prodcount = 0
		prodcount = prodcount+1
		db.child('userAPI').child('prodcount').set(prodcount)
		x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
		now = datetime.datetime.now()
		date_string = now.strftime('%Y%m%d%H%M%S')
		slno ='sl'+date_string+x
		images = args['photo']
		
		del args['photo']	
		for i in images:
			if not allowed_file(i.filename):
				abort(400, message='unsupported file format')
		args['imgList'] = {}
		for img in images:
			imgCnt = db.child('userAPI').child('imgCnt').get().val()
			if imgCnt == None:
				imgCnt = 0
			imgCnt += 1
			db.child('userAPI').child('imgCnt').set(imgCnt)
			# print()
			count = images.index(img)
			# print(str(img) in images)
			# for j in len(images):
			imgName = slno+str(count)
			storage.child('userAPI').child('productImage').child(slno).child(imgName).put(img)
			imgUrl = storage.child('userAPI').child('productImage').child(slno).child(imgName).get_url(None)
			args['imgList'][imgName] = {'imgUrl' : imgUrl}
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist==None:
			productlist={}
		productlist[slno] = args
		db.child('userAPI').child('productlist').set(productlist)
		# return args
		productCount=db.child('userAPI').child('prodcount').get().val()
		if productCount==None:
			productCount = 0
		productCount = productCount + 1
		if productlist==None:
			productlist={}
		return productCount

	def get(self):
		productlist=db.child('userAPI').child('productlist').get().val()
		productCount=db.child('userAPI').child('prodcount').get().val()
		# productSlNo=db.child('userAPI').child('prodcount').get().val()
		# print(productCount)
		if productCount==None:
			productCount = 0
		productCount = productCount + 1
		
		if productlist==None:
			productlist={}
		response = {'productCount':productCount, 'productlist':productlist}
		return response

class UserUpdate(Resource):
	def get(self,userID):
		args = userupdateparser.parse_args()
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		return userList

	def post(self, userID):
		userID = userID.upper()
		args = userupdateparser.parse_args()
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		if userID in userList:
			if args['name']:
				userList[userID]['name'] = args['name']
			if args['email']:
				userList[userID]['email'] = args['email']
			if args['mobile']:
				userList[userID]['mobile'] = args['mobile']
			if args['password']:
				userList[userID]['password'] = args['password']
			if args['photo']:
				storage.child('HouseRentalPortal').child('userImage').child(userID).child('pic.jpg').put(args['photo'])
				userList[userID]['imgUrl'] = storage.child('HouseRentalPortal').child('userImage').child(userID).child('pic.jpg').get_url(None)
			db.child('userAPI').child('userList').set(userList)
		else:
			abort(400, message='user not found')
		return userList

class ProductUpdate(Resource):
	def get(self,slno):
		print(slno)
		productlist=db.child('userAPI').child('productlist').get().val()
		res = db.child('userAPI').child('productlist').child(slno)
		res.remove()
		prodcount = db.child('userAPI').child('prodcount').get().val()
		db.child('userAPI').child('prodcount').set(prodcount - 1)
		# productlist['sl'+str(prodcount+1)] = 'sl'+str(prodcount - 1)
		if productlist==None:
			productlist={}
		return prodcount

	def post(self,slno):
		args = productupdateparser.parse_args()
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist==None:
			productlist={}
		if slno in productlist:
			if args['productname']:
				productlist[slno]['productname'] = args['productname']
			if args['category']:
				productlist[slno]['category'] = args['category']
			if args['gender']:
				productlist[slno]['gender'] = args['gender']
			if args['productRate']:
				productlist[slno]['productRate'] = args['productRate']
			if args['smallCount']:
				productlist[slno]['smallCount'] = args['smallCount']
			if args['lCount']:
				productlist[slno]['lCount'] = args['lCount']
			if args['xlCount']:
				productlist[slno]['xlCount'] = args['xlCount']
			if args['offerprice']:
				productlist[slno]['offerprice'] = args['offerprice']
			if args['color']:
				productlist[slno]['color'] = args['color']
			if args['material']:
				productlist[slno]['material'] = args['material']
			if args['pincode']:
				productlist[slno]['pincode'] = args['pincode']
			if args['specifications']:
				productlist[slno]['specifications'] = args['specifications']
			if args['category']:
				productlist[slno]['category'] = args['category']
			db.child('userAPI').child('productlist').set(productlist)
		else:
			abort(400, message='product not found')
		return productlist

def gender(f1):
	productlist=db.child('userAPI').child('productlist').get().val()
	if productlist==None:
		productlist={}
	filterlist = {}
	for i in productlist:
		for j in f1:
			if productlist[i]['gender'] == j: 
				filterlist[i] = productlist[i]
	return filterlist

def category(f1):
	productlist=db.child('userAPI').child('productlist').get().val()
	if productlist==None:
		productlist={}
	filterlist = {}
	for i in productlist:
		for j in f1:
			if productlist[i]['category'] == j: 
				filterlist[i] = productlist[i]
	return filterlist

def color(f1):
	productlist=db.child('userAPI').child('productlist').get().val()
	if productlist==None:
		productlist={}
	filterlist = {}
	
	for i in productlist:
		for j in f1:
			if productlist[i]['color'] == j: 
				filterlist[i] = productlist[i]
	return filterlist

class FilterCategories(Resource):
	def post(self,options):
		options = options.split('*&*')
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist==None:
			productlist={}

		categoryList = []
		colorList = []
		materialList = []
		filterList = {}

		for i in productlist:
			if productlist[i]['category'] not in categoryList:
				categoryList.append(productlist[i]['category'])
			if productlist[i]['color'] not in colorList:
				colorList.append(productlist[i]['color'])
			if productlist[i]['material'] not in materialList:
				materialList.append(productlist[i]['material'])
		
		for i in options:
			li = []
			for k in productlist:
				if i in categoryList:
					if i in productlist[k]['category']:
						li.append(k)
				else:
					if i in productlist[k]['category']:
						li.append(k)
			
				if i in colorList:
					if i in productlist[k]['color']:
						li.append(k)
				else:
					if i in productlist[k]['color']:
						li.append(k)
			
				if i in materialList:
					if i in productlist[k]['material']:
						li.append(k)
				else:
					if i in productlist[k]['material']:
						li.append(k)
			filterList[i] = li
		print(filterList)
		r = []
		c =[]
		m = []

		catList = []
		colList = []
		matList = []
		filteredList = {}

		for i in filterList:
			if i in categoryList:
				r.append(filterList[i])
			elif i in colorList:
				c.append(filterList[i])
			elif i in materialList:
				m.append(filterList[i])
	
		for i in r:
			for j in i:
				catList.append(j)
		for i in c:
			for j in i:
				colList.append(j)
		for i in m:
			for j in i:
				matList.append(j)
		
		result  = []
		for i in catList:
			for j in colList:
				for k in matList:
					if i == j == k:
						filteredList[i] = productlist[i]
			
			# for i in result:
			# 	for j in matList:
			# 		if i == j:
			# 			filteredList[i] = productlist[i]
					# if i != j:
					# 	for n in result:
					# 		filteredList[n] = productlist[n]
					# else:
					# 	for n in result:
					# 		filteredList[n] = productlist[n]
							
		print(filteredList)
		return filteredList
			
									
		
			

class FilterCategoriesRate(Resource):
	def post(self):
		args = filterrateparser.parse_args()
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist==None:
			productlist={}
		for i in productlist:
			if args['catID'] == 'asc':
				filterlist = dict(sorted(productlist.items(),key=lambda x: x[1]['offerPrice']))
				break
			if args['catID'] == 'dsc':
				filterlist = dict(sorted(productlist.items(),key=lambda x: x[1]['offerPrice'],reverse=True))
				break
			if args['catID'].count('-') == 1:
				minLimit = args['catID'].split('-')[0]
				maxLimit = args['catID'].split('-')[1]
				if minLimit.isnumeric() and maxLimit.isnumeric():
					minLimit = int(minLimit)
					maxLimit = int(maxLimit)
					if minLimit != maxLimit:
						if minLimit < maxLimit:
							if productlist[i]['offerPrice'] >= minLimit and productlist[i]['offerPrice'] <= maxLimit:
								filterlist[i] = productlist[i]
					else:
						abort(400, message='minLimit should be less than maxLimit')
				else:
					abort(400, message='minLimit and maxLimit should not be equal')
			else:
				abort(400, message='limit should be a integer')
		return filterlist

class FilterCategoriesColor(Resource):
	def post(self):
		args = filtercolorparser.parse_args()
		productlist=db.child('userAPI').child('productlist').get().val()
		args['catName'] = args['catName'].lower()
		if productlist==None:
			productlist={}
		filterlist = {}
		for i in productlist:
			if args['catName'] == productlist[i]['color']:
				filterlist[i] = productlist[i]
		return filterlist

class ProductCart(Resource):
	def post(self,userID):
		args = cartparser.parse_args()
		flag = 0
		userID=userID.upper()
		slno = args['slno']
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist == None:
			productlist={}
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		cartlist = db.child('userAPI').child('cartlist').get().val()
		if cartlist == None:
			cartlist = {}
		if userID in cartlist:
			if slno in cartlist[userID]:
				cartlist[userID][slno]['quantity'] = int(cartlist[userID][slno]['quantity'])+int(args['quantity'])
			else:
				cartlist[userID][slno] = {'quantity':int(args['quantity'])}
		else:
			cartlist[userID] = {
			slno:{'quantity':int(args['quantity'])}
			}
		db.child('userAPI').child('cartlist').set(cartlist)
		return cartlist[userID]

	def get(self,userID):
		userID = userID.upper()
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		cartlist = db.child('userAPI').child('cartlist').get().val()
		if cartlist == None:
			cartlist = {}
		if userID not in cartlist:
			abort(400,message = 'user cart is empty')
		return cartlist[userID]

class ProductCartUpdate(Resource):
	def get(self,userID,slno):
		userID = userID.upper()
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist == None:
			productlist={}
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		if slno not in productlist:
			abort(400,message = 'product not found')
		cartlist = db.child('userAPI').child('cartlist').get().val()
		if cartlist == None:
			cartlist = {}
		cartitem = {}
		if userID in cartlist:
			if slno in cartlist[userID]:
				cartdetail = cartlist[userID]
				for slno in cartdetail:
					cartitem = cartdetail[slno]
		return cartitem

	def put(self,userID,slno):
		args = cartupdateparser.parse_args()
		userID = userID.upper()
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist == None:
			productlist={}
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		if slno not in productlist:
			abort(400,message = 'product not found')
		cartlist = db.child('userAPI').child('cartlist').get().val()
		if cartlist == None:
			cartlist = {}
		cartitem = {}
		if userID in cartlist:
			if slno in cartlist[userID]:
				cartdetail = cartlist[userID]
				if slno in cartdetail:
					flag = 1
					cartlist[userID][slno]['quantity'] = int(args['quantity'])
					db.child('userAPI').child('cartlist').set(cartlist)
					cartitem = cartlist[userID][slno]
		if flag == 0:
			abort(400,message = 'product not found')
		return cartitem

	def delete(self,userID,slno):
		args = cartupdateparser.parse_args()
		userID = userID.upper()
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist == None:
			productlist={}
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		if slno not in productlist:
			abort(400,message = 'product not found')
		cartlist = db.child('userAPI').child('cartlist').get().val()
		if cartlist == None:
			cartlist = {}
		cartitem = {}
		if userID in cartlist:
			if slno in cartlist[userID]:
				cartdetail = cartlist[userID]
				if slno in cartdetail:
					flag = 1
					del cartlist[userID][slno]
					db.child('userAPI').child('cartlist').set(cartlist)
		if flag == 0:
			abort(400,message = 'product not found')
		return cartlist

class CartTotalPrice(Resource):
	def post(self,userID):
		userID = userID.upper()
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist == None:
			productlist={}
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			userList = {}
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		cartlist = db.child('userAPI').child('cartlist').get().val()
		if cartlist == None:
			cartlist = {}
		cartitem = {}
		totalamount = 0
		if userID in cartlist:
			cartitem = cartlist[userID]
			for i in cartitem:
				cartitem[i]['productadd'] =  cartlist[userID][i]['quantity']*productlist[i]['offerPrice']
				totalamount += cartitem[i]['productadd']
		cart = {
			'userCart'   : cartitem,
			'grandTotal' : totalamount
		}
		return cart

class ProductWishList(Resource):
	def post(self,userID):
		args = wishparser.parse_args()
		now = datetime.datetime.now()
		date_string = now.strftime('%Y%m%d%H%M%S')
		userID=userID.upper()
		slno = args['slno']
		productlist=db.child('userAPI').child('productlist').get().val()
		if productlist == None:
			productlist={}
		offerPrice = productlist[slno]['offerPrice']
		productPrice = productlist[slno]['productPrice']
		userList = db.child('userAPI').child('userList').get().val()
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		wishlist = db.child('userAPI').child('wishlist').get().val()
		if wishlist == None:
			wishlist = {}
		if userID in wishlist:
			if slno in wishlist[userID]:
				# abort(400,message = 'product already in wishlist!')
				return 'product already in wishlist!'
			else:
				wishlist[userID][slno] = {'offer price': offerPrice,'productPrice': productPrice ,'date added': date_string}
		else:
			wishlist[userID] = {
			slno:{'offer price': offerPrice,'productPrice': productPrice ,'date added': date_string}
			}
		db.child('userAPI').child('wishlist').set(wishlist)
		return wishlist[userID]
		
	def get(self,userID):
		userID = userID.upper()
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			abort(400,message = 'userlist is empty!')
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		wishlist = db.child('userAPI').child('wishlist').get().val()
		if wishlist == None:
			wishlist = {}
		if userID not in wishlist:
			return 'wishlist is empty!'
		return wishlist[userID]

class WishlistDelete(Resource):
	# def get(self,userID,slno):
	# 	userID = userID.upper()
	# 	userList = db.child('userAPI').child('userList').get().val()
	# 	if userList == None:
	# 		abort(400,message = 'userlist is empty!')
	# 	if userID not in userList:
	# 		abort(400,message = 'user does not exist !')
	# 	wishlist = db.child('userAPI').child('wishlist').get().val()
	# 	if wishlist == None:
	# 		wishlist = {}
	# 	if userID not in wishlist:
	# 		abort(400,message = 'wishlist is empty!')
	# 	if slno in wishlist[userID]:
	# 		wishitem = wishlist[userID][slno]
	# 	return wishitem

	def delete(self,userID,slno):
		userID = userID.upper()
		userList = db.child('userAPI').child('userList').get().val()
		if userList == None:
			abort(400,message = 'userlist is empty!')
		if userID not in userList:
			abort(400,message = 'user does not exist !')
		wishlist = db.child('userAPI').child('wishlist').get().val()
		if wishlist == None:
			wishlist = {}
		if userID not in wishlist:
			return 'wishlist is empty!'
		if userID in wishlist:
			if slno in wishlist[userID]:
				del wishlist[userID][slno]
		db.child('userAPI').child('wishlist').set(wishlist)
		return wishlist[userID]


			
api.add_resource(AdminLogin, '/adminLogin')
api.add_resource(UserReg, '/user')
api.add_resource(UserLogin, '/userlogin')
api.add_resource(productReg,'/product')
api.add_resource(UserUpdate, '/user/<userID>')
api.add_resource(ProductUpdate,'/product/<slno>')
api.add_resource(FilterCategories,'/products/filter/<options>')
api.add_resource(FilterCategoriesRate, '/products/filterrate')
api.add_resource(FilterCategoriesColor, '/products/filtercolor')
api.add_resource(bannerAdd, '/admin/bannerAdd')
api.add_resource(ProductCart, '/cart/<userID>')
api.add_resource(ProductCartUpdate, '/cart/<userID>/<slno>')
api.add_resource(CartTotalPrice, '/totalprice/<userID>')
api.add_resource(ProductWishList, '/wishlist/<userID>')
api.add_resource(WishlistDelete, '/wishlist/<userID>/<slno>')

