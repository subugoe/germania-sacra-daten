<?xml version='1.0' encoding='UTF-8'?>
<!--
	XSL hack to let us transport structured XML data in Solr fields.

	It assumes that the field »xml« contains valid XML and inserts it into
	the resulting document without escaping.

	This is likely to  break in bad ways if the field »xml« does not contain
	XML or if the postprocessing expects nothing but flat Solr documents.

	To use this, place the XSL in the »xslt« subfolder of your Solr »conf« folder
	and invoke the XSLT Response writer for this XSL by using
		wt=xslt&tr=xmlpassthrough.xsl
	in the request URL.

	Sven-S. Porst, SUB Göttignen <porst@sub.uni-goettingen.de>
-->
<xsl:stylesheet
	version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:saxon="http://saxon.sf.net/">

	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="arr[@name='xml']/str">
		<str>
			<xsl:copy-of select="saxon:parse(.)"/>
		</str>
	</xsl:template>

</xsl:stylesheet>