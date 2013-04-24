package org.dialang.exporter.db

import java.sql.{DriverManager,Connection}

import scala.collection.JavaConversions._
import scala.collection.mutable.{ListBuffer,HashMap,ArrayBuffer}

import org.dialang.common.model.Item

class DB {

  Console.setOut(System.err)

  Class.forName("org.postgresql.Driver")
  val conn = DriverManager.getConnection("jdbc:postgresql:DIALANG","dialangadmin","dialangadmin")

  val vsptLevels = List("V1","V2","V3","V4","V5","V6")
  val saSkills = List("Reading","Writing","Listening")

  // TODO: This should not be needed. All db access should happen in here.
  def getConnection = conn

  def getAdminLanguageLocales = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT locale FROM admin_languages")
    val locales = new ListBuffer[String]
    while(rs.next) {
      locales += rs.getString("locale")
    }
    rs.close
    st.close
    locales.toList
  }

  // TODO: Cache this
  def getAdminLanguages = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT * FROM admin_languages")
    val map = new HashMap[String,Any]
    val languages = new ListBuffer[Map[String,String]]
    while(rs.next) {
      languages += Map("locale" -> rs.getString("locale"),"description" -> rs.getString("description"))
    }
    map += ("languages" -> languages)
    map += ("fundermessage" -> "The DIALANG Project is being carried out with the support of the commission of the European Communities within the framework of the SOCRATES programme, LINGUA 2")
    rs.close
    st.close
    map.toMap
  }

  // TODO: Cache this
  def getTranslation(key:String,language:String) = {
    val st = conn.createStatement
    var rs = st.executeQuery("SELECT value FROM display_texts WHERE key = '" + key + "' and locale = '" + language + "'")
    var translation = ""
    if(rs.next) {
        translation = rs.getString("value")
    }
    rs.close
    st.close
    translation
  }

  def getTranslationLike(key:String,language:String) = {
    val st = conn.createStatement
    var rs = st.executeQuery("SELECT value FROM display_texts WHERE key LIKE '" + key + "' and locale = '" + language + "'")
    var translation = ""
    if(rs.next) {
        translation = rs.getString("value")
    }
    rs.close
    st.close
    translation
  }

  // TODO: Cache this
  def getTestLanguagePrompts(adminLanguageCode:String) = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT * FROM display_texts WHERE key like 'ChooseTest_Language%' and locale = '" + adminLanguageCode + "'")
    val map = new HashMap[String,String]
    while(rs.next) {
        val languageDescription = rs.getString("value")
        val vk = rs.getString("key")
        val languageCode = vk.substring(vk.indexOf("#") + 1)
        map += (languageCode.toLowerCase -> languageDescription)
    }

    rs.close
    st.close
    map.toMap
  }

  // TODO: Cache this
  def getTestLanguageCodes = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT locale FROM test_languages")
    val list = new ListBuffer[String]
    while(rs.next) {
        list += rs.getString("locale")
    }

    rs.close
    st.close
    list.toList
  }

  // TODO: Cache this
  def getVSPTWords(tl: String) = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT word,words.word_id AS id,valid FROM vsp_test_word,words WHERE locale = '" + tl + "' AND vsp_test_word.word_id = words.word_id")

    val list = new ListBuffer[(String,String,Boolean)]
    while(rs.next) {
        list += ((rs.getString("word"),rs.getString("id"),rs.getBoolean("valid")))
    }

    rs.close()
    st.close()

    list.toList
  }

  def getSAStatements(al: String, skill: String) = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT * FROM sa_statements WHERE locale = '" + al + "' AND skill = '" + skill + "'")

    val list = new ListBuffer[Map[String,String]]
    while(rs.next) {
        list += Map("wid" -> rs.getString("wid"),"statement" -> rs.getString("statement"))
    }

    rs.close()
    st.close()

    list.toList
  }

  def getBaskets = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT * FROM baskets")
    //val rs = st.executeQuery("SELECT * FROM baskets WHERE type = 'tabbedpane'")

    val list = new ListBuffer[Basket]

    while(rs.next) {
      list += new Basket(rs)
    }

    rs.close()
    st.close()

    list.toList
  }

  def getChildBaskets(testletId:Int) = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT * FROM baskets WHERE parent_basket_id = " + testletId)

    val list = new ListBuffer[Basket]

    while(rs.next) {
      list += new Basket(rs)
    }

    rs.close()
    st.close()

    list.toList
  }

  def getItemsForBasket(basketId:Int) = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT items.* FROM baskets,basket_item,items WHERE baskets.id = " + basketId + " AND baskets.id = basket_item.basket_id AND basket_item.item_id = items.id")

    val list = new ListBuffer[Item]

    while(rs.next) {
      list += new Item(rs)
    }

    rs.close()
    st.close()

    list.toList
  }

  def getAnswersForItem(itemId:Int) = {
    val st = conn.createStatement
    val rs = st.executeQuery("SELECT * FROM answers WHERE item_id = " + itemId)

    val list = new ListBuffer[Map[String,String]]

    while(rs.next) {
      list += Map( "id" -> rs.getInt("id").toString,
                    "item_id" -> rs.getInt("item_id").toString,
                    "text" -> rs.getString("text"),
                    "correct" -> rs.getInt("correct").toString )
    }

    rs.close()
    st.close()

    list.toList
  }

  def getLevels = {

    val st = conn.createStatement
    val rs = st.executeQuery("SELECT level FROM levels")

    val list = new ListBuffer[String]

    while(rs.next) {
      list += rs.getString(1)
    }

    rs.close()
    st.close()

    list.toList
  }
}
