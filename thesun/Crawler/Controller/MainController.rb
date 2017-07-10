require 'rubygems'
require 'mechanize'

require_relative 'StringController'
require_relative 'HouseController'

class MainController
	def ping_link link
		return false if link == nil
		page = @mechanize.get(link)
		return true if page.code.to_i == 200
		return false
	end

	def get_data page
		houses = page.parser.css('div.a-item.a-list-item.a-storage-live')
		return false if houses.count == 0

		houses.each do |house|
			id = house["data-id"]
			puts id if HouseController.exists?(id)
			HouseController.loadHouse(id) unless HouseController.exists?(id)
		end

		return true
	end

	def initialize link
		@mechanize = Mechanize.new

		if ping_link(link) == false then
			puts "No internet connection"
			return
		end

		if ping_link("https://krisha.kz") == false then
			puts "Cannot reach krisha.kz"
			return
		end
	end

	def start 
		for i in 1..2000 do
			link = "https://krisha.kz/prodazha/kvartiry/almaty"\
				   "/?das[_sys.hasphoto]=1&das[who]=2&page=#{i}"
			
			puts "Started parsing #{StringController.countable(i)} page"
			page = @mechanize.get(link)

			if page.code.to_i != 200 then
				puts "Failed to load #{StringController.countable(i)} page"
				return
			end

			if get_data(page) == false then
				puts "Failed to parse #{StringController.countable(i)} page"
				return
			end

			puts "Finished parsing #{StringController.countable(i)} page"
		end
	end
end

controller = MainController.new "https://krisha.kz/"
controller.start