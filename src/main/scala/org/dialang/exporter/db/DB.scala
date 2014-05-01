package org.dialang.exporter.db

import java.sql.{DriverManager,Connection,SQLException,Statement}

import java.io.{FileInputStream, InputStreamReader}
import java.util.Properties

import scala.collection.JavaConversions._
import scala.collection.mutable.{ListBuffer,HashMap,ArrayBuffer}

import org.dialang.common.model.{Item, ScoredItem}

import org.slf4j.LoggerFactory

class DB {

  private val logger = LoggerFactory.getLogger(getClass)

  Console.setOut(System.err)

  Class.forName("org.postgresql.Driver")
  val conn = DriverManager.getConnection("jdbc:postgresql:DIALANG","dialangadmin","dialangadmin")

  val tlForBasketST = conn.prepareStatement("SELECT tl FROM preest_assignments WHERE booklet_id = (SELECT booklet_id FROM booklet_basket WHERE basket_id = ? LIMIT 1)")

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

  val adminTexts: Map[String, Properties] = {
      val builder = Map.newBuilder[String, Properties]
      for (al <- getAdminLanguageLocales) {
        // Load the Properties for this locale
        val props = new Properties
        props.load(new InputStreamReader(new FileInputStream("admin-texts/admintexts_" + al + ".properties"), "UTF-8"))
        builder += (al -> props)
      }
      builder.result
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
      map += ("fundermessage" -> "The original DIALANG Project was carried out with the support of the commission of the European Communities within the framework of the SOCRATES programme, LINGUA 2")
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

  def getTranslation(key: String, language: String) = {

    adminTexts.get(language) match {
      case Some(p: Properties) => p.getProperty(key)
      case _ => {
        // language not found
        println("Language: '" + language + "' not found.")
        ""
      }
    }
  }

  def getTranslationLike(keyExpression: String,language: String) = {

    val parts = keyExpression.split("%")

    adminTexts.get(language) match {
      case Some(p: Properties) => {
        p.find(t => t._1.startsWith(parts(0)) && t._1.endsWith(parts(1)) ) match {
          case Some((k: String, v: String)) => v
          case _ => {
            println("No value found for expression: '" + keyExpression + "'.")
            ""
          }
        }
      }
      case _ => {
        // language not found
        println("Language: '" + language + "' not found.")
        ""
      }
    }
  }

  def getSubSkills(al: String): Map[String,String] = {

    adminTexts.get(al) match {
      case Some(p: Properties) => {
        val matches = p.filter(_._1.startsWith("Subskill#")).toMap
        matches.map( t => {
          val subskillCode = t._1.substring(t._1.indexOf("#") + 1).toLowerCase
          (subskillCode -> t._2)
        })
      }
      case _ => {
        // language not found
        println("Language: '" + al + "' not found.")
        Map()
      }
    }
  }

  def getTestLanguagePrompts(al: String): Map[String, String] = {

    adminTexts.get(al) match {
      case Some(p: Properties) => {
        val matches = p.filter(_._1.startsWith("ChooseTest_Language")).toMap
        matches.map( t => {
          val languageCode = t._1.substring(t._1.indexOf("#") + 1).toLowerCase
          (languageCode -> t._2)
        })
      }
      case _ => {
        // language not found
        println("Language: '" + al + "' not found.")
        Map()
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

  def getTestLanguageForBasket(id: Int): Option[String] = {

    try {
      tlForBasketST.setInt(1, id)
      val rs = tlForBasketST.executeQuery

      val tl = {
          if (rs.next) {
            Some(rs.getString("tl"))
          } else {
            None
          }
        }
      rs.close()
      tl
    } catch {
      case e:Exception => {
        logger.error("Caught exception while getting test language.", e)
        None
      }
    }
  }
}
