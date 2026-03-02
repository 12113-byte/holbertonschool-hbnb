
	def _name_validation(self, string, string_name):
		if string is None or len(string) == 0:
			raise TypeError(f"{string_name} must not be empty")

		if isinstance(string, str) is False:
			raise TypeError(f"{string_name} must be a string")

		if len(string) > 50:
			raise ValueError(f"{string_name} is too long (<= 50 characters)")

		return string

	def _email_validation(self, email):
			if email is None or len(email) == 0:
				raise TypeError("Email must not be empty")

			return email



	def _rating_validation(self, rating)
		if rating is None:
			raise TypeError("Rating cannot be empty")
		if isinstance(rating, int) is False:
			raise TypeError("Rating must be an int")
		if rating < 1 or rating > 5:
			raise ValueError("Rating cannot be less than 1 or greater than 5")

		return rating



		def _price_validation(self, price):
		if price is None:
			raise TypeError("Price cannot be empty")

		if isinstance(price, float) is False:
			raise TypeError("Price must be a float")

		if price < 1:
			raise ValueError("Price must be a postive value")

	return price

	def _title_validation(self, string):
		if string is None or len(string) == 0:
			raise TypeError("Title must not be empty")

		if isinstance(string, str) is False:
			raise TypeError("Title must be a string")

		if len(string) > 100:
			raise ValueError("Title is too long (<= 100 characters)")

		return string


	def _lat_validation(self, latitude):
		if latitude is None:
			raise TypeError("Latitude cannot be empty")

		if isinstance(latitude, float) is False:
			raise TypeError("Latitude must be a float")

		if latitude < -90 or latitude > 90:
			raise ValueError("Latitude must be valid (between -90 and 90)")

		return latitude

	def _long_validation(self, longitude):
		if longitude is None:
			raise TypeError("Longitude cannot be empty")

		if isinstance(longitude, float) is False:
			raise TypeError("Longitude must be a float")

		if longitude < -180 or longitude > 180:
			raise ValueError("Longitude must be valid (between -180 and 180)")

		return longitude
