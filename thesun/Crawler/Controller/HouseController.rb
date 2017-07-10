require 'rubygems'
require 'mechanize'
require 'mysql'

require_relative 'StringController'
require_relative '../Model/House'

class HouseController
	@@mechanize = Mechanize.new
	@@house     = House.new

	def self.exists? id
		result = false
		begin
	    	con = Mysql.new 'localhost', 'askar', '', 'KRISHA_DATA'
	    	rs = con.query("SELECT id FROM Houses WHERE id=#{id}")
	    	n_rows = rs.num_rows
	    	result = true if n_rows > 0
		rescue Mysql::Error => e
		    puts e.errno
		    puts e.error    
		ensure
		    con.close if con
		end
		return result
	end

	def self.print_info
		puts @@house.id
		puts @@house.room_number
		puts @@house.address    
		puts @@house.price      
		puts @@house.region
		puts @@house.map_complex		
		puts @@house.house_type        
		puts @@house.built_time        
		puts @@house.floor             
		puts @@house.all_space         
		puts @@house.living_space      
		puts @@house.kitchen_space  
		puts @@house.state         
		puts @@house.bathroom          
		puts @@house.balcony           
		puts @@house.balcony_is_glazed 
		puts @@house.door            
		puts @@house.phone
		puts @@house.internet  
		puts @@house.parking           
		puts @@house.furniture          
		puts @@house.flooring          
		puts @@house.ceiling           
		puts @@house.safety            
		puts @@house.at_the_hostel
		puts @@house.description_option
		puts @@house.description_text
	end

	def self.loadHouse id
		@@house = House.new
		@@page = @@mechanize.get("https://krisha.kz/a/show/#{id}")

		@@house.id                  = "#{id}"
		@@house.room_number         = load_room_number()
		@@house.address             = load_address()
		@@house.price               = load_price()
		@@house.region			    = load_region()
		@@house.map_complex	        = load_map_complex()
		@@house.house_type          = load_house_type()
		@@house.built_time          = load_built_time()
		@@house.floor               = load_floor()
		@@house.all_space           = load_all_space()
		@@house.living_space        = load_living_space()
		@@house.kitchen_space       = load_kitchen_space()
		@@house.state               = load_state()
		@@house.bathroom            = load_bathroom()
		@@house.balcony             = load_balcony()
		@@house.balcony_is_glazed   = load_balcony_is_glazed()
		@@house.door                = load_door()
		@@house.phone		        = load_phone()
		@@house.internet            = load_internet()
		@@house.parking             = load_parking()
		@@house.furniture           = load_furniture()
		@@house.flooring            = load_flooring()
		@@house.ceiling             = load_ceiling()
		@@house.safety              = load_safety()
		@@house.at_the_hostel       = load_at_the_hostel()
		@@house.description_option  = load_description_option()
		@@house.description_text    = load_description_text()

		print_info
		@@house.save
	end

	def self.load_room_number
		fields = @@page.parser.css("div.a-header h1")
		return "" if fields.count == 0
		
		title = fields[0].text
		StringController.before(title, "-комнатная квартира, ")
	end

	def self.load_address
		fields = @@page.parser.css("div.a-header h1")
		return "" if fields.count == 0

		title = fields[0].text
		StringController.after(title, "-комнатная квартира, ")
	end

	def self.load_price
		fields = @@page.parser.css("div.a-header span.price")
		return "" if fields.count == 0
		
		fields[0].text
	end

	def self.load_region
		fields = @@page.parser.css("div.main-col.a-item div.a-where-region")
		return "" if fields.count == 0
		
		fields[0].text
	end

	def self.load_map_complex
		load_field_with_name('Жилой комплекс')
	end

	def self.load_house_type
		type_and_time = load_field_with_name("Дом")

		return "" unless type_and_time.include?(", ")
		return StringController.before(type_and_time, ", ")
	end

	def self.load_built_time
		type_and_time = load_field_with_name('Дом')

		return type_and_time unless type_and_time.include?(', ')
		return StringController.before(StringController.after(type_and_time, ', '), ' г.п.')
	end

	def self.load_floor
		load_field_with_name('Этаж')
	end

	def self.load_all_space
		all_and_living_and_kitchen = load_field_with_name('Площадь')
		return StringController.before(all_and_living_and_kitchen, ', ')
	end

	def self.load_living_space
		all_and_living_and_kitchen = load_field_with_name('Площадь')
		living_and_kitchen = StringController.after(all_and_living_and_kitchen, ', ')
		
		current = StringController.before(living_and_kitchen, ', ')
		return StringController.after(current, '— ') if current.include? 'жилая'

		current = StringController.after(living_and_kitchen, ', ')
		return StringController.after(current, '— ') if current.include? 'жилая'

		return '' 
	end

	def self.load_kitchen_space
		all_and_living_and_kitchen = load_field_with_name('Площадь')
		living_and_kitchen = StringController.after(all_and_living_and_kitchen, ', ')
		
		current = StringController.before(living_and_kitchen, ', ')
		return StringController.after(current, '— ') if current.include? 'кухня'

		current = StringController.after(living_and_kitchen, ', ')
		return StringController.after(current, '— ') if current.include? 'кухня'

		return '' 
	end

	def self.load_state
		load_field_with_name('Состояние')
	end

	def self.load_bathroom
		load_field_with_name('Санузел')
	end

	def self.load_balcony
		load_field_with_name('Балкон')
	end

	def self.load_balcony_is_glazed
		load_field_with_name('Балкон остеклен')
	end

	def self.load_door
		load_field_with_name('Дверь')
	end

	def self.load_phone
		load_field_with_name('Телефон')
	end

	def self.load_internet
		load_field_with_name('Интернет')
	end

	def self.load_parking
		load_field_with_name('Парковка')
	end

	def self.load_furniture
		load_field_with_name('Мебель')
	end

	def self.load_flooring
		load_field_with_name('Пол')
	end
	
	def self.load_ceiling
		load_field_with_name('Потолки')
	end

	def self.load_safety
		load_field_with_name('Безопасность')
	end
	
	def self.load_at_the_hostel
		load_field_with_name('В прив. общежитии')
	end

	def self.load_description_option
		StringController.removeExtraWhitespaces(
			@@page.parser.css('div.col-sm-6.col-xs-6.a-description '\
							  'div.a-options-text.a-text-white-spaces').text)
	end

	def self.load_description_text
		StringController.removeExtraWhitespaces(
			@@page.parser.css('div.col-sm-6.col-xs-6.a-description '\
							  'div.a-text.a-text-white-spaces').text)
	end

	def self.load_field_with_name name
		fields = @@page.parser.css("div.col-sm-6.col-xs-6.a-description dl.a-parameters dt")

		fields.each do |field|
			return field.css('~dd')[0].text if field.text.include? name
		end		
		return ''
	end
end