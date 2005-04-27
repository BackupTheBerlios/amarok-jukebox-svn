import os
import apsw
import random

import Debug

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
		return self.__checkCount('tags', 'url', url)

	def isCover(self, url):
		# FIXME: special hack for covers under .kde
		if url.startswith(os.getenv('HOME')+'/.kde/share/apps/amarok/albumcovers/'):
			return True
		return self.__checkCount('images', 'path', url)

	def __checkCount(self, table, field, value):
		(count, ) = self.select("count(*) FROM %s WHERE %s = \"%s\""
					% (table, field, value)).next()
		return (count > 0)

	def albumCover(self, artist, album):
		# FIXME: This doesn't catch all covers; it seems that there are others
		# in .kde/share/apps/amarok that do not appear in the database
		r = self.select("path FROM images WHERE artist = \"%s\" AND album = \"%s\""
				% (artist.decode('utf-8'), album.decode('utf-8')))
		try:
			(url, ) =  r.next()
			return url
		except:
			return None

	def songDetails(self, song):
		result = {}
		try:
			(artist, album, genre, title, year, comment, track, bitrate, length, samplerate) = self.select("artist.name, album.name, genre.name, tags.title, year.name, tags.comment, tags.track, tags.bitrate, tags.length, tags.samplerate FROM tags, artist, album, year, genre WHERE url = \"%s\" AND tags.artist = artist.id AND tags.album = album.id AND tags.year = year.id AND tags.genre = genre.id" % song).next()
			result['artist'] = artist
			result['album'] = album
			result['genre'] = genre
			result['title'] = title
			result['year'] = year
			result['comment'] = comment
			result['track'] = track
			result['bitrate'] = bitrate
			length = int(length)
			result['length'] = "%d:%02d" % (length / 60, length % 60)
			result['samplerate'] = samplerate
		except:
			return None
		return result

	def randomSong(self):
		(count, ) = self.select("count(*) FROM tags").next()
		(url, ) = self.select("url FROM tags LIMIT 1 OFFSET %s" % random.randint(0, count-1)).next()
		Debug.log("Random song: " + url)
		return url
