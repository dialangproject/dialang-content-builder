package org.dialang.exporter.db

import java.sql.ResultSet

class Basket(rs: ResultSet) {

  val id = rs.getInt("id")
  val basketType = rs.getString("type")
  val skill = rs.getString("skill")
  val parentTestletId = rs.getInt("parent_testlet_id")
  val parentTestletPosition = rs.getInt("parent_testlet_position")
  val prompt = rs.getString("prompt")
  val gaptext = rs.getString("gaptext")
  val mediatype = rs.getString("mediatype")
  val textmedia = rs.getString("textmedia")
  val filemedia = rs.getString("filemedia")
}
