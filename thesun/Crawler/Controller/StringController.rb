class StringController
	def self.countable number
		if number % 10 == 1 && number % 100 != 11 then
			return "#{number}st"
		elsif number % 10 == 2 && number % 100 != 12 then
			return "#{number}nd"
		elsif number % 10 == 3 && number % 100 != 13 then
			return "#{number}rd"
		else
			return "#{number}th"
		end
	end

	def self.before(str, query)
		pos = str.length
		for i in 0...str.length
			found = true
			for j in 0...query.length
				found = false if i + j >= str.length
				found = false if str[i + j] != query[j]
			end
			if found then
				pos = i
				break
			end
		end

		result = ""
		for i in 0...pos
			result += str[i]
		end

		return result
	end

	def self.after(str, query)
		pos = str.length
		for i in 0...str.length
			found = true
			for j in 0...query.length
				found = false if i + j >= str.length
				found = false if str[i + j] != query[j]
			end
			if found then
				pos = i + query.length
				break
			end
		end

		result = ""
		for i in pos...str.length
			result += str[i]
		end

		return result
	end

	def self.removeExtraSpaces str
		result = ""
		i = 0
		while i < str.length
			if str[i] == ' ' then
				j = i
				while j + 1 < str.length and str[j + 1] == ' '
					j += 1
				end
				result += str[i]
				i = j + 1
			else
				result += str[i]
				i += 1
			end
		end
		return result
	end

	def self.removeExtraWhitespaces str
		result = ""
		i = 0
		while i < str.length
			if str[i] == ' ' or str[i] == '\t' or str[i] == '\n' then
				j = i
				while j + 1 < str.length and str[j + 1] == str[i]
					j += 1
				end
				result += str[i]
				i = j + 1
			else
				result += str[i]
				i += 1
			end
		end
		return result
	end
end