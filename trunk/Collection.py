import os
import sqlite
import random

import Debug

class Collection:
        def __init__(self):
                self.__cx = sqlite.connect(os.getenv('HOME')+'/.kde/share/apps/amarok/collection.db', encoding='utf-8')
		self.__cu = self.__cx.cursor()

        def __select(self, query):
		self.__cu.execute("SELECT %s" % query)

	def __fetchone(self):
		return self.__cu.fetchone()

	def __fetchall(self):
		return self.__cu.fetchall()

	def artists(self, filter = '%'):
		self.__select("id, name FROM artist WHERE name LIKE '%s' ORDER BY name"
			    % filter)
		return self.__fetchall()

	def getName(self, source, id):
		self.__select("name FROM %s WHERE id = %s" % (source, id))
		(name, ) = self.__fetchone()
		return name

	def albumsByArtist(self, id):
		self.__select("DISTINCT album.id, album.name FROM album, tags WHERE tags.artist = %s AND album.id = tags.album ORDER BY album.name"
			    % id)
		return self.__fetchall()

	def songsByAlbum(self, id):
		self.__select("url, title FROM tags WHERE album = %s ORDER BY track"
			    % id)
		return self.__fetchall()

	def songTitle(self, url):
		d = self.songDetails(url)
		return d['title']

	def inCollection(self, url):
		return self.__checkCount('tags', 'url', url)

	def isCover(self, url):
		# FIXME: special hack for covers under .kde
		if url.startswith(os.getenv('HOME')+'/.kde/share/apps/amarok/albumcovers/'):
			return True
		return self.__checkCount('images', 'path', url)

	def __checkCount(self, table, field, value):
		self.__select("count(*) FROM %s WHERE %s = \"%s\""
			    % (table, field, value))
		(count, ) = self.__fetchone()
		return (count > 0)

	def albumCover(self, artist, album):
		# FIXME: This doesn't catch all covers; it seems that there are others
		# in .kde/share/apps/amarok that do not appear in the database
		self.__select("path FROM images WHERE artist = \"%s\" AND album = \"%s\""
			    % (artist, album))
		try:
			(url, ) =  self.__fetchone()
			return url
		except:
			return None

	def songDetails(self, song):
		result = {}
		try:
			self.__select("artist.name, album.name, genre.name, tags.title, year.name, tags.comment, tags.track, tags.bitrate, tags.length, tags.samplerate FROM tags, artist, album, year, genre WHERE url = \"%s\" AND tags.artist = artist.id AND tags.album = album.id AND tags.year = year.id AND tags.genre = genre.id" % song)
			(artist, album, genre, title, year, comment, track, bitrate, length, samplerate) = self.__fetchone()
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
		self.__select("count(*) FROM tags")
		(count, ) = self.__fetchone()
		self.__select("url FROM tags LIMIT 1 OFFSET %s" % random.randint(0, count-1))
		(url, ) = self.__fetchone()
		Debug.log("Random song: " + url)
		return url
