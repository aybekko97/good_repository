require 'mysql'

class House
	attr_accessor :id
	attr_accessor :room_number
	attr_accessor :address
	attr_accessor :price
	attr_accessor :region
	attr_accessor :map_complex
	attr_accessor :house_type
	attr_accessor :built_time
	attr_accessor :floor
	attr_accessor :all_space
	attr_accessor :living_space
	attr_accessor :kitchen_space
	attr_accessor :state
	attr_accessor :bathroom          
	attr_accessor :balcony           
	attr_accessor :balcony_is_glazed 
	attr_accessor :door     
	attr_accessor :phone
    attr_accessor :internet     
	attr_accessor :parking           
	attr_accessor :furniture          
	attr_accessor :flooring          
	attr_accessor :ceiling           
	attr_accessor :safety            
	attr_accessor :at_the_hostel     
	attr_accessor :description_option
	attr_accessor :description_text       


	def save
		begin
	    con = Mysql.new 'localhost', 'askar', '', 'KRISHA_DATA'
	    con.query("INSERT INTO Houses(id, \
	    							  room_number, \
	    							  address, \
	    							  price, \
	    							  region, \
	    							  map_complex, \
	    							  house_type, \
	    							  built_time, \
	    							  floor, \
	    							  all_space, \
	    							  living_space, \
	    							  kitchen_space, \
	    							  state, \
	    							  bathroom, \
	    							  balcony, \
	    							  balcony_is_glazed, \
	    							  door, \
	    							  phone, \
	    							  internet, \
	    							  parking, \
	    							  furniture, \
	    							  flooring, \
	    							  ceiling, \
	    							  safety, \
	    							  at_the_hostel, \
	    							  description_option, \
	    							  description_text) \
	                VALUES(#{id}, \
	                	   '#{room_number}', \
	                	   '#{address}', \
	                	   '#{price}', \
	                	   '#{region}', \
	                	   '#{map_complex}', \
	                	   '#{house_type}', \
	                	   '#{built_time}', \
	                	   '#{floor}', \
	                	   '#{all_space}', \
	                	   '#{living_space}', \
	                	   '#{kitchen_space}', \
	                	   '#{state}', \
	                	   '#{bathroom}', \
	                	   '#{balcony}', \
	                	   '#{balcony_is_glazed}', \
	                	   '#{door}', \
	                	   '#{phone}', \
	                	   '#{internet}', \
	                	   '#{parking}', \
	                	   '#{furniture}', \
	                	   '#{flooring}', \
	                	   '#{ceiling}', \
	                	   '#{safety}', \
	                	   '#{at_the_hostel}', \
	                	   '#{description_option}', \
	                	   '#{description_text}' \
	                	   )")
		rescue Mysql::Error => e
		    puts e.errno
		    puts e.error    
		ensure
		    con.close if con
		end
	end
end
