package org.dialang.exporter

import java.sql.{Connection,Statement,SQLException}

import org.dialang.exporter.db.DB

object DisplayTextsDumper extends App {

  val db = new DB
  var conn:Connection = null
  var st:Statement = null
  
  try {
    conn = db.getConnection
    st = conn.createStatement
    val rs = st.executeQuery("SELECT * FROM display_texts WHERE locale = '" + args(0) + "'")
    while(rs.next) {
      val value = rs.getString("value")
      System.out.println(rs.getString("key") + "=" + rs.getString("value"))
      //System.out.println()
    }
    rs.close
  } finally {
    if(st != null) {
      try {
        st.close
      } catch { case e:SQLException => }
    }

    if(conn != null) {
      try {
        conn.close
      } catch { case e:SQLException => }
    }
  }
}
