package org.dialang.exporter.db

import java.sql.{DriverManager,Connection,SQLException,Statement}

import scala.collection.JavaConversions._
import scala.collection.mutable.{ListBuffer,HashMap,ArrayBuffer}

import org.dialang.common.model.{Item, ScoredItem}

class DB {

  Console.setOut(System.err)

  Class.forName("org.postgresql.Driver")
  val conn = DriverManager.getConnection("jdbc:postgresql:DIALANG","dialangadmin","dialangadmin")

  val saSkills = List("Reading","Writing","Listening")

  val testSkills = List("Reading","Writing","Listening","Structures","Vocabulary")

  val advfbSkills = List("Reading","Writing","Listening")

  // TODO: This should not be needed. All db access should happen in here.
  def getConnection = conn

  def cleanup() {
    if (conn != null) {
      conn.close()
    }
  }

  def getAdminLanguageLocales = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT locale FROM admin_languages")
      val locales = new ListBuffer[String]
      while (rs.next) {
        locales += rs.getString("locale")
      }
      rs.close
      locales.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getAdminLanguages = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT * FROM admin_languages")
      val map = new HashMap[String,Any]
      val languages = new ListBuffer[Map[String,String]]
      while (rs.next) {
        languages += Map("locale" -> rs.getString("locale"),"description" -> rs.getString("description"))
      }
      map += ("languages" -> languages)
      map += ("fundermessage" -> "The DIALANG Project was carried out with the support of the commission of the European Communities within the framework of the SOCRATES programme, LINGUA 2")
      rs.close
      map.toMap
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getTranslation(key:String,language:String) = {
    var st:Statement = null
    try {
      st = conn.createStatement
      var rs = st.executeQuery("SELECT value FROM display_texts WHERE key = '" + key + "' and locale = '" + language + "'")
      var translation = ""
      if (rs.next) {
        translation = rs.getString("value")
      }
      rs.close
      translation
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getTranslationLike(key:String,language:String) = {
    var st:Statement = null
    try {
      st = conn.createStatement
      var rs = st.executeQuery("SELECT value FROM display_texts WHERE key LIKE '" + key + "' and locale = '" + language + "'")
      var translation = ""
      if (rs.next) {
        translation = rs.getString("value")
      }
      rs.close
      translation
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getSubSkills(adminLanguageCode:String) = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT * FROM display_texts WHERE key like 'Subskill#%' and locale = '" + adminLanguageCode + "'")
      val map = new HashMap[String,String]
      while (rs.next) {
        val subskillDescription = rs.getString("value")
        val vk = rs.getString("key")
        val subskillCode = vk.substring(vk.indexOf("#") + 1)
        map += (subskillCode.toLowerCase -> subskillDescription)
      }

      rs.close()
      map.toMap
    } finally {
      if (st != null) {
        try {
          st.close()
        } catch { case e:SQLException => }
      }
    }
  }

  def getTestLanguagePrompts(adminLanguageCode:String):Map[String,String] = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT * FROM display_texts WHERE key like 'ChooseTest_Language%' and locale = '" + adminLanguageCode + "'")
      val map = new HashMap[String,String]
      while (rs.next) {
        val languageDescription = rs.getString("value")
        val vk = rs.getString("key")
        val languageCode = vk.substring(vk.indexOf("#") + 1)
        map += (languageCode.toLowerCase -> languageDescription)
      }

      rs.close
      map.toMap
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getTestLanguageCodes:List[Tuple2[String,String]] = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT locale,two_letter_code FROM test_languages")
      val list = new ListBuffer[Tuple2[String,String]]
      while (rs.next) {
        list += ((rs.getString("locale"),rs.getString("two_letter_code")))
      }
      rs.close
      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getVSPTWords(tl: String) = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT word,words.word_id AS id,valid FROM vsp_test_word,words WHERE locale = '" + tl + "' AND vsp_test_word.word_id = words.word_id")

      val list = new ListBuffer[(String,String,Boolean)]
      while (rs.next) {
        list += ((rs.getString("word"),rs.getString("id"),rs.getBoolean("valid")))
      }

      rs.close()

      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getSAStatements(al: String, skill: String) = {

    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT * FROM sa_statements WHERE locale = '" + al + "' AND skill = '" + skill + "' ORDER BY wid")

      val list = new ListBuffer[Map[String,String]]
      while (rs.next) {
        list += Map("wid" -> rs.getString("wid"), "statement" -> rs.getString("statement"))
      }

      rs.close()
      st.close()

      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getBaskets = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT * FROM baskets")
      //val rs = st.executeQuery("SELECT * FROM baskets WHERE type = 'tabbedpane'")

      val list = new ListBuffer[Basket]

      while (rs.next) {
        list += new Basket(rs)
      }

      rs.close()

      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getChildBaskets(testletId:Int) = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT * FROM baskets WHERE parent_testlet_id = " + testletId)

      val list = new ListBuffer[Basket]

      while (rs.next) {
        list += new Basket(rs)
      }

      rs.close()

      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getItemsForBasket(basketId:Int) = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT i.*,bi.position FROM baskets b,basket_item bi,items i WHERE b.id = " + basketId + " AND b.id = bi.basket_id AND bi.item_id = i.id ORDER BY position")

      val list = new ListBuffer[ScoredItem]

      while (rs.next) {
        val item = new ScoredItem(new Item(rs))
        item.positionInBasket = rs.getInt("position")
        list += item
      }

      rs.close()
      st.close()

      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getAnswersForItem(itemId:Int) = {
    var st:Statement = null
    try {
      st = conn.createStatement
      val rs = st.executeQuery("SELECT * FROM answers WHERE item_id = " + itemId)

      val list = new ListBuffer[Map[String,String]]

      while (rs.next) {
        list += Map( "answerId" -> rs.getInt("id").toString,
                    "item_id" -> rs.getInt("item_id").toString,
                    "text" -> rs.getString("text"),
                    "correct" -> rs.getInt("correct").toString )
      }

      rs.close()

      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getVSPLevels = {
    var st:Statement = null
    try {
      st = conn.createStatement

      val rs = st.executeQuery("SELECT level FROM vsp_levels")

      val list = new ListBuffer[String]

      while (rs.next) {
        list += rs.getString(1)
      }

      rs.close()

      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }

  def getItemLevels = {
    var st:Statement = null
    try {
      st = conn.createStatement

      val rs = st.executeQuery("SELECT level FROM item_levels")

      val list = new ListBuffer[String]

      while (rs.next) {
        list += rs.getString(1)
      }

      rs.close()

      list.toList
    } finally {
      if (st != null) {
        try {
          st.close
        } catch { case e:SQLException => }
      }
    }
  }
}
