<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="xml" indent="yes" omit-xml-declaration="yes" />
	<xsl:template match="/response">
		<xsl:for-each select="/response/lst[@name='facet_counts']/lst[@name='facet_fields']/lst/int">
<xsl:value-of select="@name" /><xsl:text>
</xsl:text>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
