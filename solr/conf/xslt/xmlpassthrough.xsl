<?xml version='1.0' encoding='UTF-8'?>
<!--
	XSL hack to let us transport structured XML data in Solr fields.

	It assumes that the <str> field »xml« contains valid XML, replaces the
	<str> tag by an <xml> tag and includes the field content without escaping.

	To use this, place the XSL in the »xslt« subfolder of your Solr »conf« folder
	and invoke the XSLT Response writer [1] for this XSL by using
		wt=xslt&tr=xmlpassthrough.xsl
	in the request URL.
	
	Edit the second tempate’s match attribute to use this on other fields.

	[1] http://wiki.apache.org/solr/XsltResponseWriter

	2013 Sven-S. Porst, SUB Göttignen <porst@sub.uni-goettingen.de>
-->
<xsl:stylesheet version='1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>

	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="arr[@name='xml']/str">
		<xml>
			<xsl:value-of disable-output-escaping="yes" select="." />
		</xml>
	</xsl:template>

</xsl:stylesheet>