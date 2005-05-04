import os
import os.path
import random
import md5

import Dcop
import Debug

class Collection:

	__coverHome = os.getenv('HOME')+'/.kde/share/apps/amarok/albumcovers/'

        def __select(self, query):
		# FIXME: this needs to be converted to python-dcop, but I'm having some
		# encoding problems: it seems that query with non-ASCII characters just
		# don't work; see using-python-dcop branch
		# This is bug #105084
		# http://bugs.kde.org/show_bug.cgi?id=105084
		r = Dcop.call("collection query \"SELECT %s\"" % query.replace('"', '\\"'))
		r = r.split("\n")
		nargs = len(query.split("FROM")[0].split(","))
		self.__results = [ ]
		while len(r) > 0:
			a = [ ]
			for i in range(nargs):
				a.append(r.pop(0))
			self.__results.append(a)

	def __fetchone(self):
		return self.__results.pop(0)

	def __fetchall(self):
		r = self.__results
		self.__results = [ ]
		return r

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
		# FIXME: amaroK bug #104769
		if d is None:
			return url
		else:
			return d['title']

	def inCollection(self, url):
		return self.__checkCount('tags', 'url', url)

	def isCover(self, url):
		if url.startswith(self.__coverHome):
			return True
		return self.__checkCount('images', 'path', url)

	def __checkCount(self, table, field, value):
		self.__select("count(*) FROM %s WHERE %s = \"%s\""
			    % (table, field, value))
		(count, ) = self.__fetchone()
		return (count > 0)

	def albumCover(self, artist, album):
		self.__select("path FROM images WHERE artist = \"%s\" AND album = \"%s\""
			    % (artist, album))
		try:
			(url, ) =  self.__fetchone()
			if url == "":
				raise Exception
		except:
			d = md5.new()
			# FIXME: this only seems to work on ASCII
			# Original code uses: artist.lower().local8Bit()
			d.update(artist.lower())
			d.update(album.lower())
			url = self.__coverHome + 'large/' + d.hexdigest()
			print url
			if not os.path.isfile(url):
				return None
		return url

	def songDetails(self, song):
		result = {}
		try:
			self.__select("artist.name, album.name, genre.name, tags.title, year.name, tags.track, tags.bitrate, tags.length, tags.samplerate FROM tags, artist, album, year, genre WHERE url = \"%s\" AND tags.artist = artist.id AND tags.album = album.id AND tags.year = year.id AND tags.genre = genre.id" % song)
			(artist, album, genre, title, year, track, bitrate, length, samplerate) = self.__fetchone()
			result['artist'] = artist
			result['album'] = album
			result['genre'] = genre
			result['title'] = title
			result['year'] = year
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
		self.__select("url FROM tags LIMIT 1 OFFSET %s" % random.randint(0, int(count)-1))
		(url, ) = self.__fetchone()
		Debug.log("Random song: " + url)
		return url
