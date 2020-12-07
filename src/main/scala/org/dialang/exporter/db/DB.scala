package org.dialang.exporter.db

import java.sql.{DriverManager,Connection,SQLException,Statement}

import java.io.{FileInputStream, InputStreamReader}
import java.util.Properties

import scala.jdk.CollectionConverters._
import scala.collection.mutable.{ListBuffer,HashMap,ArrayBuffer}

import org.dialang.common.model.{Item, ScoredItem}

import org.slf4j.LoggerFactory

class DB {

  private val logger = LoggerFactory.getLogger(getClass)

  //Console.setOut(System.err)

  Class.forName("org.postgresql.Driver")
  val conn = DriverManager.getConnection("jdbc:postgresql:DIALANG","dialangadmin","dialangadmin")

  val adminLocalesST= conn.prepareStatement("SELECT locale FROM admin_languages")
  val adminLanguagesST = conn.prepareStatement("SELECT * FROM admin_languages")
  val tlForBasketST = conn.prepareStatement("SELECT tl FROM preest_assignments WHERE booklet_id = (SELECT booklet_id FROM booklet_basket WHERE basket_id = ? LIMIT 1)")
  val testLanguagesST = conn.prepareStatement("SELECT locale,two_letter_code FROM test_languages")
  val vsptWordST = conn.prepareStatement("SELECT word,words.word_id AS id,valid FROM vsp_test_word,words WHERE locale = ? AND vsp_test_word.word_id = words.word_id")
  val saStatementsST= conn.prepareStatement("SELECT * FROM sa_statements WHERE locale = ? AND skill = ? ORDER BY wid")
  val basketsST = conn.prepareStatement("SELECT * FROM baskets")
  val childBasketsST = conn.prepareStatement("SELECT * FROM baskets WHERE parent_testlet_id = ?")
  val basketItemsST = conn.prepareStatement("SELECT i.*,bi.position FROM baskets b,basket_item bi,items i WHERE b.id = ? AND b.id = bi.basket_id AND bi.item_id = i.id ORDER BY position")
  val itemAnswersST = conn.prepareStatement("SELECT * FROM answers WHERE item_id = ?")
  val vspLevelsST = conn.prepareStatement("SELECT level FROM vsp_levels")
  val itemLevelsST = conn.prepareStatement("SELECT level FROM item_levels")

  val saSkills = List("Reading","Writing","Listening")

  val testSkills = List("Reading","Writing","Listening","Structures","Vocabulary")

  val advfbSkills = List("Reading","Writing","Listening")

  def getConnection = conn

  def cleanup() {

    adminLocalesST.close()
    adminLanguagesST.close()
    tlForBasketST.close()
    testLanguagesST.close()
    vsptWordST.close()
    saStatementsST.close()
    basketsST.close()
    childBasketsST.close()
    basketItemsST.close()
    itemAnswersST.close()
    vspLevelsST.close()
    itemLevelsST.close()

    if (conn != null) {
      conn.close()
    }
  }

  val adminTexts: Map[String, Map[String, String]] = {

      val builder = Map.newBuilder[String, Map[String,String]]
      for (al <- getAdminLanguageLocales) {
        // Load the Properties for this locale
        val props = new Properties
        props.load(new InputStreamReader(new FileInputStream("admin-texts/admintexts_" + al + ".properties"), "UTF-8"))
        builder += (al -> props.asScala.toMap)
      }
      builder.result
    }

  def getAdminLanguageLocales = {

    val rs = adminLocalesST.executeQuery
    val locales = new ListBuffer[String]
    while (rs.next) {
      locales += rs.getString("locale")
    }
    rs.close
    locales.toList
  }

  def getAdminLanguages = {

    val rs = adminLanguagesST.executeQuery
    val languages = new ListBuffer[Map[String,String]]
    while (rs.next) {
      languages += Map("locale" -> rs.getString("locale"),"description" -> rs.getString("description"))
    }
    rs.close
    val map = new HashMap[String,Any]
    map += ("languages" -> languages.toList)
    map += ("fundermessage" -> "The original DIALANG Project was carried out with the support of the commission of the European Communities within the framework of the SOCRATES programme, LINGUA 2")
    map.toMap
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
      case Some(p: Map[String, String]) => {
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
      case Some(p: Map[String, String]) => {
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
      case Some(p: Map[String, String]) => {
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

  def getTestLanguageCodes: List[(String, String)] = {

    val rs = testLanguagesST.executeQuery
    val list = new ListBuffer[Tuple2[String, String]]
    while (rs.next) {
      list += ((rs.getString("locale"), rs.getString("two_letter_code")))
    }
    rs.close
    list.toList
  }

  def getVSPTWords(tl: String): List[(String, String, Boolean)] = {

    vsptWordST.setString(1 , tl)
    val rs = vsptWordST.executeQuery

    val list = new ListBuffer[(String,String,Boolean)]
    while (rs.next) {
      list += ((rs.getString("word"),rs.getString("id"),rs.getBoolean("valid")))
    }

    rs.close()

    list.toList
  }

  def getSAStatements(al: String, skill: String) = {

    saStatementsST.setString(1, al)
    saStatementsST.setString(2, skill)
    val rs = saStatementsST.executeQuery

    val list = new ListBuffer[Map[String,String]]
    while (rs.next) {
      list += Map("wid" -> rs.getString("wid"), "statement" -> rs.getString("statement"))
    }

    rs.close()
    list.toList
  }

  def getBaskets = {

    val rs = basketsST.executeQuery

    val list = new ListBuffer[Basket]

    while (rs.next) {
      list += new Basket(rs)
    }

    rs.close()

    list.toList
  }

  def getChildBaskets(testletId: Int) = {

    childBasketsST.setInt(1, testletId)

    val rs = childBasketsST.executeQuery

    val list = new ListBuffer[Basket]

    while (rs.next) {
      list += new Basket(rs)
    }

    rs.close()

    list.toList
  }

  def getItemsForBasket(basketId: Int) = {

    basketItemsST.setInt(1, basketId)

    val rs = basketItemsST.executeQuery

    val list = new ListBuffer[ScoredItem]

    while (rs.next) {
      val rsi = new Item(rs)
      //val item = new ScoredItem(item.id, item.itemType, item.skill, item.subskill, item.text, item.weight)
      val item = new ScoredItem(rsi.id, rsi.itemType, rsi.skill, rsi.subskill, rsi.text, rsi.weight)
      item.positionInBasket = rs.getInt("position")
      list += item
    }

    rs.close()

    list.toList
  }

  def getAnswersForItem(itemId: Int) = {

    itemAnswersST.setInt(1, itemId)
    val rs = itemAnswersST.executeQuery

    val list = new ListBuffer[Map[String,String]]

    while (rs.next) {
      list += Map( "answerId" -> rs.getInt("id").toString,
                  "item_id" -> rs.getInt("item_id").toString,
                  "text" -> rs.getString("text"),
                  "correct" -> rs.getInt("correct").toString )
    }

    rs.close()

    list.toList
  }

  def getVSPLevels = {

    val rs = vspLevelsST.executeQuery

    val list = new ListBuffer[String]

    while (rs.next) {
      list += rs.getString(1)
    }

    rs.close()

    list.toList
  }

  def getItemLevels = {

    val rs = itemLevelsST.executeQuery

    val list = new ListBuffer[String]

    while (rs.next) {
      list += rs.getString(1)
    }

    rs.close()

    list.toList
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
