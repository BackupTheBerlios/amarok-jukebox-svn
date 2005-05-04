<xsl:stylesheet version="1.0"
		xmlns="http://www.w3.org/1999/xhtml"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!--
  <xsl:output
      method="xml"
      doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
      doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
      />
-->
  <xsl:template match="item">
    <dt>
      <xsl:if test="@queue_index">
	<xsl:attribute name="id">playing</xsl:attribute>
      </xsl:if>
      <span class="artist">
	<xsl:value-of select="Artist"/>
      </span>
      -
      <span class="title">
	<xsl:value-of select="Title"/>
      </span>
    </dt>
    <dd>
      <xsl:if test="@queue_index">
	<xsl:attribute name="id">playing</xsl:attribute>
      </xsl:if>
      <span class="album">
	<xsl:value-of select="Album"/>
      </span>
      -
      <span class="length">
	<xsl:value-of select="Length"/>
      </span>
    </dd>
  </xsl:template>

  <xsl:template match="/">
<!--    <html>
      <head>
	<title>amaroK playlist</title>
      </head>
      <body>-->
        <h1>Playlist</h1>
	<dl>
	  <xsl:apply-templates />
	</dl>
	<form action='playlist' method='post'>
	  <input type='submit' name='clear' value='Clear Play List' />
	  <input type='submit' name='clearAndStop'
		 value='Clear Play List And Stop Player' />
	</form>
<!--	<hr />
	<address><a href='..'>Home</a></address>
      </body>
    </html>-->
  </xsl:template>

</xsl:stylesheet>
