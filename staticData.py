jrxmlSnips = {
	"textFieldIntro" : '			<textField isStretchWithOverflow="true" isBlankWhenNull="true" evaluationTime="Now" hyperlinkType="None"  hyperlinkTarget="Self" >\n',
	"textFieldOutro" : '			</textField>\n',
	"textExpression" : '				<textFieldExpression  class="java.lang.String"><![CDATA["{cont}"]]></textFieldExpression>\n',
	"reportElement" : '''				<reportElement
					style="{style}"
					x="{x}"
					y="{y}"
					width="{linewidth}"
					height="{lineheight}"
					key="{key}"
					positionType="Float"
					isPrintRepeatedValues="false"
					isRemoveLineWhenBlank="true"/>
				<box></box>
				<textElement>
					<font/>
				</textElement>\n''',
	"groupIntro" : '''		<group  name="{groupName}" >
			<groupExpression><![CDATA[]]></groupExpression>\n''',
	"groupHeaderIntro" : '''			<groupHeader>
			<band height="{height}"  isSplitAllowed="true" >\n''',
	"groupFooterIntro" : '''			</band>
			</groupHeader>
			<groupFooter>
			<band height="{height}"  isSplitAllowed="true" >\n''',
	"groupOutro" : '''			</band>
			</groupFooter>\n''',
	"reportIntro" : '''<?xml version="1.0" encoding="UTF-8"  ?>
<!-- Created with iReport - A designer for JasperReports -->
<!DOCTYPE jasperReport PUBLIC "//JasperReports//DTD Report Design//EN" "http://jasperreports.sourceforge.net/dtds/jasperreport.dtd">
<jasperReport
		 name="{reportName}"
		 columnCount="1"
		 printOrder="Vertical"
		 orientation="{orientation}"
		 pageWidth="{pageWidth}"
		 pageHeight="{pageHeight}"
		 columnWidth="{columnWidth}"
		 columnSpacing="0"
		 leftMargin="56"
		 rightMargin="56"
		 topMargin="0"
		 bottomMargin="22"
		 whenNoDataType="AllSectionsNoDetail"
		 isTitleNewPage="false"
		 isSummaryNewPage="false">
	<property name="ireport.zoom" value="1.0" />
	<property name="ireport.x" value="0" />
	<property name="ireport.y" value="0" />
	<property name="ireport.scriptlethandling" value="0" />
	<property name="ireport.encoding" value="UTF-8" />
	<import value="java.util.*" />
	<import value="net.sf.jasperreports.engine.*" />
	<import value="net.sf.jasperreports.engine.data.*" />
	<template><![CDATA["stl:///styles/Table.jrtx"]]></template>
	<template><![CDATA["stl:///styles/Text.jrtx"]]></template>
	<template><![CDATA["stl:///styles/Title.jrtx"]]></template>\n''',
	"reportOutro" : '</jasperReport>\n', 
}
