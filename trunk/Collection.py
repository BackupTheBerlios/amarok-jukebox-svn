import os
import apsw
import random

class Collection:
        def __init__(self):
                self.__cx = apsw.Connection(os.getenv('HOME')+'/.kde/share/apps/amarok/collection.db')
		self.__cu = self.__cx.cursor()

        def select(self, query):
		q = "SELECT %s" % query
		return self.__cu.execute(q)

	def artists(self, filter = '%'):
		return self.select("id, name FROM artist WHERE name LIKE '%s' ORDER BY name"
				   % filter)

	def getName(self, source, id):
		(name, ) = self.select("name FROM %s WHERE id = %s" % (source, id)).next()
		return name

	def albumsByArtist(self, id):
		return self.select("DISTINCT album.id, album.name FROM album, tags WHERE tags.artist = %s AND album.id = tags.album ORDER BY album.name"
				   % id)

	def songsByAlbum(self, id):
		return self.select("url, title FROM tags WHERE album = %s ORDER BY track"
				   % id)

	def getSongTitle(self, url):
		(title, ) = self.select("title FROM tags WHERE url = \"%s\"" % url).next()
		return title

	def inCollection(self, url):
		(count, ) = self.select("count(*) FROM tags WHERE url = \"%s\"" % url).next()
		return (count > 0)

	def randomSong(self):
		(count, ) = self.select("count(*) FROM tags").next()
		(url, ) = self.select("url FROM tags LIMIT 1 OFFSET %s" % random.randint(0, count-1)).next()
		return url
