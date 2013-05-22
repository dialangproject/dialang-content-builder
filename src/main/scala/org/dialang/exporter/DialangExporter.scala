package org.dialang.exporter

import org.fusesource.scalate._

import org.dialang.exporter.db.DB

import java.io.{File,FileOutputStream,OutputStreamWriter}
import java.util.regex.{Pattern,Matcher}

import scala.collection.JavaConversions._
import scala.collection.mutable.{ListBuffer,HashMap,ArrayBuffer}

object DialangExporter extends App {

  Console.setOut(System.out)

  val db = new DB
  val engine = new TemplateEngine
  val websiteDir = new File("website")

  if(!websiteDir.exists) {
    websiteDir.mkdirs();
  }

  val adminLanguages = db.getAdminLanguageLocales
  /*
  exportAls()
  exportLegendPages(adminLanguages)
  exportFlowchartPages(adminLanguages)
  */
  exportTLSPages(adminLanguages)
  /*
  exportVSPTIntroPages(adminLanguages)
  exportVSPTPages(adminLanguages)
  exportVSPTFeedbackPages(adminLanguages)
  exportSAIntroPages(adminLanguages)
  exportSAPages(adminLanguages)
  exportTestIntroPages(adminLanguages)
  exportBasketPages(adminLanguages)
  exportEndOfTestPages(adminLanguages)
  exportFeedbackMenuPages(adminLanguages)
  exportSAFeedbackPages(adminLanguages)
  exportTestResultPages(adminLanguages)
  exportItemReviewPages(adminLanguages)
  */

  db.cleanup()

  sys.exit()

  def exportAls() {
    val output = engine.layout("src/main/resources/als.mustache",db.getAdminLanguages)
    val alsFile = new OutputStreamWriter(new FileOutputStream(new File(websiteDir,"als.html")),"UTF-8")
    alsFile.write(output)
    alsFile.close()
  }

  def exportLegendPages(adminLanguages:List[String]) {

    val legendDir = new File(websiteDir,"legend")
    if(!legendDir.isDirectory) {
        legendDir.mkdirs()
    }

    for(al <- adminLanguages) { 
        val key = db.getTranslation("Title_Key",al)
        val welcome = db.getTranslation("Title_WelcomeDIALANG",al)
        val next = db.getTranslation("Caption_ContinueNext",al)
        val back = db.getTranslation("Caption_BackPrevious",al)
        val skipf = db.getTranslation("Caption_SkipNextSection",al)
        val skipb = db.getTranslation("Caption_SkipPreviousSection",al)
        val yes = db.getTranslation("Caption_Yes",al)
        val no = db.getTranslation("Caption_No",al)
        val help = db.getTranslation("Caption_Help",al)
        val smiley = db.getTranslation("CaptionInstantOnOff",al)
        val keyboard = db.getTranslation("Caption_AdditionalCharacters",al)
        val speaker = db.getTranslation("Caption_PlaySound",al)
        val prevtooltip = db.getTranslation("Caption_BacktoALS",al)
        val nexttooltip = db.getTranslation("Caption_ContinueNext",al)
        val map = Map("key" -> key,"next" -> next,"back" -> back,"welcome" -> welcome,"skipf" -> skipf,"skipb" -> skipb,"yes" -> yes,"no" -> no,"help" -> help,"smiley" -> smiley,"keyboard" -> keyboard,"speaker" -> speaker,"prevtooltip" -> prevtooltip,"nexttooltip" -> nexttooltip,"al" -> al)
        val output = engine.layout("src/main/resources/legend.mustache",map)
        val legendFile = new OutputStreamWriter(new FileOutputStream(new File(legendDir,al + ".html")),"UTF-8")
        legendFile.write(output)
        legendFile.close()
    }
  }

  def exportFlowchartPages(adminLanguages:List[String]) {

    val flowchartDir = new File(websiteDir,"flowchart")
    if(!flowchartDir.isDirectory) {
        flowchartDir.mkdirs()
    }

    for(al <- adminLanguages) { 
      val welcomeTitle = db.getTranslation("Title_WelcomeDIALANG",al)
      val welcomeText = db.getTranslation("Welcome_Intro_Text",al)
      val procedureTitle = db.getTranslation("Title_ProcedureCAPS",al)
      val procedureText = db.getTranslation("Welcome_Procedure_Text",al)
      val prevtooltip = db.getTranslation("Caption_BacktoWelcome",al)
      val nexttooltip = db.getTranslation("Caption_GotoChooseTest",al)
      val stage1Title = db.getTranslation("Title_ChooseTest",al)
      val stage1 = db.getTranslation("Welcome_Chart_ChooseTest_Text",al)
      val stage2Title = db.getTranslation("Title_Placement",al)
      val stage2 = db.getTranslation("Welcome_Chart_Placement_Text",al)
      val stage3Title = db.getTranslation("Title_SelfAssess",al)
      val stage3 = db.getTranslation("Welcome_Chart_SelfAssess_Text",al)
      val stage4Title = db.getTranslation("Title_LangTest",al)
      val stage4 = db.getTranslation("Welcome_Chart_LangTest_Text",al)
      val stage5Title = db.getTranslation("Title_FeedbackResultsAdvice",al)
      val stage5 = db.getTranslation("Welcome_Chart_Feedback_Text",al)
      val map = Map("al" -> al,
                      "welcomeTitle" -> welcomeTitle,
                      "welcomeText" -> welcomeText,
                      "procedureTitle" -> procedureTitle,
                      "procedureText" -> procedureText,
                      "stage1Title" -> stage1Title,
                      "stage1" -> stage1,
                      "stage2Title" -> stage2Title,
                      "stage2" -> stage2,
                      "stage3Title" -> stage3Title,
                      "stage3" -> stage3,
                      "stage4Title" -> stage4Title,
                      "stage4" -> stage4,
                      "stage5Title" -> stage5Title,
                      "stage5" -> stage5,
                      "prevtooltip" -> prevtooltip,
                      "nexttooltip" -> nexttooltip )
      val output = engine.layout("src/main/resources/flowchart.mustache",map)
      val flowchartFile = new OutputStreamWriter(new FileOutputStream(new File(flowchartDir,al + ".html")),"UTF-8")
      flowchartFile.write(output)
      flowchartFile.close
    }
  }

  def exportTLSPages(adminLanguages:List[String]) {

    val tlsDir = new File(websiteDir,"tls")
    if(!tlsDir.isDirectory) {
        tlsDir.mkdirs()
    }

    for(al <- adminLanguages) { 
      val skipbtooltip = db.getTranslation("Caption_BacktoALS",al)
      val prevtooltip = db.getTranslation("Caption_BacktoWelcome",al)
      val tlsTitle = db.getTranslation("Title_ChooseTest",al)
      val listeningTooltip = db.getTranslation("ChooseTest_Skill#Listening",al)
      val writingTooltip = db.getTranslation("ChooseTest_Skill#Writing",al)
      val readingTooltip = db.getTranslation("ChooseTest_Skill#Reading",al)
      val structuresTooltip = db.getTranslation("ChooseTest_Skill#Structures",al)
      val vocabularyTooltip = db.getTranslation("ChooseTest_Skill#Vocabulary",al)

      // For the disclaimer dialog box
      val disclaimerTitle = db.getTranslation("Title_UseMisuse",al)
      val disclaimer = db.getTranslation("Disclaimer_UseMisuse",al)

      // For the test confirmation dialog box
      val testChosen = db.getTranslation("Dialogues_TestSelected",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)

      val ok = db.getTranslation("Caption_OK",al)
      val done = db.getTranslation("Caption_Done",al)
      val available = db.getTranslation("Caption_Available",al)
      val notavailable = db.getTranslation("Caption_NotAvailable",al)

      val tlsMap = db.getTestLanguagePrompts(al)

      var testRows = new ListBuffer[Map[String,String]]
      tlsMap.foreach(t => {
        testRows += Map("languageName" -> t._2,"languageCode" -> t._1)
      })

      val map = Map("al" -> al,
                      "tlsTitle" -> tlsTitle,
                      "testrows" -> testRows.toList,
                      "skipbtooltip" -> skipbtooltip,
                      "prevtooltip" -> prevtooltip,
                      "listeningTooltip" -> listeningTooltip,
                      "writingTooltip" -> writingTooltip,
                      "disclaimerTitle" -> disclaimerTitle,
                      "disclaimer" -> disclaimer,
                      "testChosen" -> testChosen,
                      "yes" -> yes,
                      "no" -> no,
                      "ok" -> ok,
                      "done" -> done,
                      "available" -> available,
                      "notavailable" -> notavailable,
                      "readingTooltip" -> readingTooltip,
                      "structuresTooltip" -> structuresTooltip,
                      "vocabularyTooltip" -> vocabularyTooltip )
      val output = engine.layout("src/main/resources/tls.mustache",map)
      val tlsFile = new OutputStreamWriter(new FileOutputStream(new File(tlsDir,al + ".html")),"UTF-8")
      tlsFile.write(output)
      tlsFile.close
    }
  }

  def exportVSPTIntroPages(adminLanguages:List[String]) {

    val vsptIntroDir = new File(websiteDir,"vsptintro")
    if(!vsptIntroDir.isDirectory) vsptIntroDir.mkdirs()

    val testLanguages = db.getTestLanguageCodes

    for(al <- adminLanguages) { 
      val prevtooltip = db.getTranslation("Caption_BacktoChooseTest",al)
      val nexttooltip = db.getTranslation("Caption_StartPlacement",al)
      val skipftooltip = db.getTranslation("Caption_SkipPlacement",al)
      val title = db.getTranslation("Title_Placement",al)
      val text = db.getTranslation("PlacementIntro_Text",al)

      // Confirmation dialog texts.
      val warningText = db.getTranslation("Dialogues_SkipPlacement",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)

      val map = Map("al" -> al,
                  "title" -> title,
                  "text" -> text,
                  "warningText" -> warningText,
                   "yes" -> yes,
                   "no" -> no,
                  "nexttooltip" -> nexttooltip,
                  "prevtooltip" -> prevtooltip,
                  "skipftooltip" -> skipftooltip )
      val output = engine.layout("src/main/resources/vsptintro.mustache",map)
      val vsptIntroFile = new OutputStreamWriter(new FileOutputStream(new File(vsptIntroDir,al + ".html")),"UTF-8")
      vsptIntroFile.write(output)
      vsptIntroFile.close
    }
  }

  def exportVSPTPages(adminLanguages:List[String]) {
    val vsptDir = new File(websiteDir,"vspt")
    val testLanguages = db.getTestLanguageCodes
    for(al <- adminLanguages) { 
      val alDir = new File(vsptDir,al)
      if(!alDir.isDirectory) {
        alDir.mkdirs()
      }

      val submit = db.getTranslation("Caption_SubmitAnswers",al)
      val title = db.getTranslation("Title_Placement",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)
      val confirmSend = db.getTranslation("Dialogues_Submit",al)
      val skipftooltip = db.getTranslation("Caption_QuitPlacement",al)

      // Confirmation dialog texts.
      val warningText = db.getTranslation("Dialogues_SkipPlacement",al)

      for(tl <- testLanguages) { 
        val wordList = db.getVSPTWords(tl)

        val tabList = new ListBuffer[Map[String,String]]
        val words = new ListBuffer[Map[String,String]]

        val validMap = new HashMap[String,Boolean]

        val wi = wordList.iterator
        while(wi.hasNext) {
          var wordTuple = wi.next
          val word1 = wordTuple._1
          val id1 = wordTuple._2
          validMap += (id1 -> wordTuple._3)
          words += Map("id" -> id1)

          wordTuple = wi.next
          val word2 = wordTuple._1
          val id2 = wordTuple._2
          validMap += (id2 -> wordTuple._3)
          words += Map("id" -> id2)

          wordTuple = wi.next
          val word3 = wordTuple._1
          val id3 = wordTuple._2
          validMap += (id3 -> wordTuple._3)
          words += Map("id" -> id3)

          tabList += Map("word1" -> word1,"id1" -> id1,
                "word2" -> word2,"id2" -> id2,
                "word3" -> word3,"id3" -> id3)
        }

        val map = Map( "al" -> al,
                        "isCorrect" -> ((compoundId:String) => {
                            val parts = compoundId.split("_")
                            val id = parts(0)
                            val response = parts(1)
                            if(validMap.get(id).get) {
                              if(response == "valid") {
                                "correct"
                              } else {
                                "incorrect"
                              }
                            } else {
                              if(response == "invalid") {
                                "correct"
                              } else {
                                "incorrect"
                              }
                            }
                          }),
                        "tl" -> tl,
                        "title" -> title,
                        "warningText" -> warningText,
                        "yes" -> yes,
                        "no" -> no,
                        "nexttooltip" -> submit,
                        "skipftooltip" -> skipftooltip,
                        "confirmsendquestion" -> confirmSend,
                        "submit" -> submit,
                        "words" -> words,
                        "tab" -> tabList.toList )
        val output = engine.layout("src/main/resources/vspt.mustache",map)
        val vsptFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,tl + ".html")),"UTF-8")
        vsptFile.write(output)
        vsptFile.close
      }
    }
  }

  def exportVSPTFeedbackPages(adminLanguages:List[String]) {
    val vsptfeedbackDir = new File(websiteDir,"vsptfeedback")
    val levels = db.getVSPLevels

    // We use this to select the correct jquery-ui tab for the level.
    val levelTabMap = Map("V1" -> 5,"V2" -> 4,"V3" -> 3,"V4" -> 2, "V5" -> 1,"V6" -> 0)

    for(al <- adminLanguages) { 
      val alDir = new File(vsptfeedbackDir,al)
      if(!alDir.isDirectory) {
        alDir.mkdirs()
      }
      val title = db.getTranslation("Title_PlacementFeedback",al)
      val yourscore = db.getTranslation("PlacementFeedback_YourScore",al)
      val nexttooltip = db.getTranslation("Caption_GotoNext",al)

      val levelv6 = db.getTranslation("PlacementFeedback_Text#V6",al)
      val levelv5 = db.getTranslation("PlacementFeedback_Text#V5",al)
      val levelv4 = db.getTranslation("PlacementFeedback_Text#V4",al)
      val levelv3 = db.getTranslation("PlacementFeedback_Text#V3",al)
      val levelv2 = db.getTranslation("PlacementFeedback_Text#V2",al)
      val levelv1 = db.getTranslation("PlacementFeedback_Text#V1",al)

      for(level <- levels) { 
        val text = db.getTranslation("PlacementFeedback_Text#" + level,al)
        val map = Map( "al" -> al,
                        "title" -> title,
                        "yourscore" -> yourscore,
                        "levelv6" -> levelv6,
                        "levelv5" -> levelv5,
                        "levelv4" -> levelv4,
                        "levelv3" -> levelv3,
                        "levelv2" -> levelv2,
                        "levelv1" -> levelv1,
                        "activeTab" -> levelTabMap.get(level),
                        "nexttooltip" -> nexttooltip,
                        "text" -> text )
        val output = engine.layout("src/main/resources/vsptfeedback.mustache",map)
        val vsptfeedbackFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,level + ".html")),"UTF-8")
        vsptfeedbackFile.write(output)
        vsptfeedbackFile.close
      }
    }
  }

  def exportSAIntroPages(adminLanguages:List[String]) {

    val saIntroDir = new File(websiteDir,"saintro")

    for(al <- adminLanguages) { 
      val alDir = new File(saIntroDir,al)
      if(!alDir.isDirectory) {
        alDir.mkdirs()
      }
      for(skill <- db.saSkills) {
        val nexttooltip = db.getTranslation("Caption_StartSelfAssess",al)
        val skipftooltip = db.getTranslation("Caption_SkipSelfAssess",al)
        val title = db.getTranslation("Title_SelfAssess#" + skill,al)
        val text = db.getTranslation("SelfAssessIntro_Text",al)

        // Confirmation dialog texts.
        val warningText = db.getTranslation("Dialogues_SkipSelfAssess",al)
        val yes = db.getTranslation("Caption_Yes",al)
        val no = db.getTranslation("Caption_No",al)

        val map = Map("al" -> al,
                    "skill" -> skill.toLowerCase,
                    "title" -> title,
                    "text" -> text,
                    "warningText" -> warningText,
                    "yes" -> yes,
                    "no" -> no,
                    "nexttooltip" -> nexttooltip,
                    "skipftooltip" -> skipftooltip )
        val output = engine.layout("src/main/resources/saintro.mustache",map)
        val saIntroFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,skill.toLowerCase + ".html")),"UTF-8")
        saIntroFile.write(output)
        saIntroFile.close
      }
    }
  }

  def exportSAPages(adminLanguages:List[String]) {

    val saDir = new File(websiteDir,"sa")

    for(al <- adminLanguages) { 
      val alDir = new File(saDir,al)
      if(!alDir.isDirectory) {
        alDir.mkdirs()
      }

      val submit = db.getTranslation("Caption_SubmitAnswers",al)
      val skipftooltip = db.getTranslation("Caption_QuitSelfAssess",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)
      val confirmSend = db.getTranslation("Dialogues_Submit",al)

      // Confirmation dialog texts.
      val warningText = db.getTranslation("Dialogues_SkipSelfAssess",al)

      for(skill <- db.saSkills) {
        val statements = db.getSAStatements(al,skill.toLowerCase)

        val title = db.getTranslation("Title_SelfAssess#" + skill,al)
        val map = Map("al" -> al,
                    "title" -> title,
                    "warningText" -> warningText,
                    "submit" -> submit,
                    "yes" -> yes,
                    "no" -> no,
                     "confirmsendquestion" -> confirmSend,
                    "statements" -> statements,
                    "skipftooltip" -> skipftooltip )
        val output = engine.layout("src/main/resources/sa.mustache",map)
        val saFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,skill.toLowerCase + ".html")),"UTF-8")
        saFile.write(output)
        saFile.close
      }
    }
  }

  def exportTestIntroPages(adminLanguages:List[String]) {

    val testIntroDir = new File(websiteDir,"testintro")
    if(!testIntroDir.isDirectory) {
        testIntroDir.mkdirs()
    }

    for(al <- adminLanguages) { 
      val nexttooltip = db.getTranslation("Caption_StartTest",al)
      val skipftooltip = db.getTranslation("Caption_SkipLangTest",al)
      val title = db.getTranslation("Title_DIALANGLangTest",al)
      val text = db.getTranslation("LangTestIntro_Text",al)
      val feedback = db.getTranslation("Caption_InstantFeedback",al)
      val instantfeedbackofftooltip = db.getTranslation("Caption_InstantFeedbackOff",al)
      val instantfeedbackontooltip = db.getTranslation("Caption_InstantFeedbackOn",al)

      // Confirmation dialog texts.
      val warningText = db.getTranslation("Dialogues_SkipLangTest",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)

      val map = Map("al" -> al,
                  "title" -> title,
                  "text" -> text,
                  "warningText" -> warningText,
                  "yes" -> yes,
                  "no" -> no,
                  "feedback" -> feedback,
                  "instantfeedbackontooltip" -> instantfeedbackontooltip,
                  "instantfeedbackofftooltip" -> instantfeedbackofftooltip,
                  "nexttooltip" -> nexttooltip,
                  "skipftooltip" -> skipftooltip )
      val output = engine.layout("src/main/resources/testintro.mustache",map)
      val saIntroFile = new OutputStreamWriter(new FileOutputStream(new File(testIntroDir,al + ".html")),"UTF-8")
      saIntroFile.write(output)
      saIntroFile.close
    }
  }

  def exportBasketPages(adminLanguages:List[String]) {

    val typeMap = Map( "gapdrop" -> "GapDrop",
                        "gaptext" -> "GapText",
                        "mcq" -> "MCQ",
                        "shortanswer" -> "ShortAnswer",
                        "tabbedpane" -> "TabbedMCQ" )

    val basketDir = new File(websiteDir,"baskets")
    if(!basketDir.isDirectory) {
        basketDir.mkdirs()
    }

    val itemPlaceholderPattern = Pattern.compile("<(\\d*)>")

    db.getBaskets.foreach(basket => {

      // Render the media markup independently of al
      val mediaMarkup = basket.mediatype match { 
          case "text/html" => {
            engine.layout("src/main/resources/textmedia.mustache",Map("markup" -> basket.textmedia))
          }
          case "audio/mpeg" => {
            engine.layout("src/main/resources/audiomedia.mustache",Map("filename" -> basket.filemedia))
          }
          case "image/jpeg" => {
            engine.layout("src/main/resources/imagemedia.mustache",Map("filename" -> basket.filemedia))
          }
          case "none" => {
            ""
          }
        }

      val basketType = basket.basketType
      val basketId = basket.id
      val skill = basket.skill
      val basketPrompt = basket.prompt

      val responseMarkup = basketType match {
          case "mcq" => {
            val item = db.getItemsForBasket(basketId).head
            val answers = db.getAnswersForItem(item.id)
            engine.layout("src/main/resources/mcqresponse.mustache",Map("itemtext" -> item.text,"itemId" -> item.id.toString,"positionInBasket" -> item.positionInBasket.toString, "answers" -> answers))
          }
          case "shortanswer" => {
            val items = db.getItemsForBasket(basketId)
            val itemList = items.map(item => {
                Map("id" -> item.id.toString,"text" -> item.text,"positionInBasket" -> item.positionInBasket.toString)
              })
            engine.layout("src/main/resources/saresponse.mustache",Map("basketPrompt" -> basketPrompt,"items" -> itemList))
          }
          case "gaptext" => {
            val gapText = basket.gaptext
            var gapMarkup = gapText

            val items = db.getItemsForBasket(basketId).map(i => {
                Map("id" -> i.id.toString,"positionInBasket" -> i.positionInBasket.toString)
              })

            val m = itemPlaceholderPattern.matcher(gapText)

            while(m.find()) {
              val itemNumber = m.group(1)
              val item = items(itemNumber.toInt)
              gapMarkup = gapMarkup.replace("<" + itemNumber + ">","<input type=\"text\" name=\"" + item.get("id").get + "-response\" />")
            }

            engine.layout("src/main/resources/gtresponse.mustache",Map("basketPrompt" -> basketPrompt,"items" -> items,"markup" -> gapMarkup))
          }
          case "gapdrop" => {
            val gapText = basket.gaptext
            var gapMarkup = gapText

            val items = db.getItemsForBasket(basketId).map(i => {
                Map("id" -> i.id.toString,"positionInBasket" -> i.positionInBasket.toString)
              })

            val m = itemPlaceholderPattern.matcher(gapText)

            while(m.find()) {
              val itemNumber = m.group(1)
              val item = items(itemNumber.toInt)
              val answers = db.getAnswersForItem(item.get("id").get.toInt)
              var select = "<select name=\"" + item.get("id").get + "-response\">"
              select += "<option></option>"
              answers.foreach(answer => {
                select += "<option value=\"" + answer.get("answerId").get + "\">" + answer.get("text").get + "</option>"
              })
              select += "</select>"
              gapMarkup = gapMarkup.replace("<" + itemNumber + ">",select)
            }

            engine.layout("src/main/resources/gdresponse.mustache",Map("basketPrompt" -> basketPrompt,"items" -> items,"markup" -> gapMarkup))
          }
          case "tabbedpane" => {

            // This is a testlet and will contain child baskets
            val childBaskets
              = db.getChildBaskets(basketId).map(childBasket => {
                  val childBasketId = childBasket.id
                  // NOTE: In the future there may be multi item baskets in a testlet. At the moment
                  // there are mainly MCQ baskets and a gap drop with one item.
                  val item = db.getItemsForBasket(childBasketId).head
                  val answers = db.getAnswersForItem(item.id)
                  Map("basketId" -> childBasketId.toString,"itemId" -> item.id.toString,"itemtext" -> item.text,"positionInBasket" -> childBasket.parentTestletPosition,"answers" -> answers)
              })

            engine.layout("src/main/resources/tabbedpaneresponse.mustache",Map("childBaskets" -> childBaskets))
          }
          case _ => {
            engine.layout("src/main/resources/mcqresponse.mustache",Map("blah" -> "blah"))
          }
        }

      for(al <- adminLanguages) {

        val alDir = new File(basketDir,al)
        if(!alDir.isDirectory) {
          alDir.mkdirs()
        }

        val rubricText = db.getTranslation("LangTest_Rubric#" + typeMap.get(basketType).get + "#Text",al)

        // Confirmation dialog texts.
        val warningText = db.getTranslation("Dialogues_SkipLangTest",al)
        val yes = db.getTranslation("Caption_Yes",al)
        val no = db.getTranslation("Caption_No",al)
        val yourAnswerTitle = db.getTranslation("LangTest_ItemFeedback_YourAnswer",al)
        val correctAnswerTitle = db.getTranslation("LangTest_ItemFeedback_CorrectAnswer",al)
        val correctAnswersTitle = db.getTranslation("LangTest_ItemFeedback_CorrectAnswers",al)
        
        val map = Map("basketId" -> basketId.toString,
                        "basketType" -> basketType,
                        "rubricText" -> rubricText,
                        "warningText" -> warningText,
                        "yes" -> yes,
                        "no" -> no,
                        "yourAnswerTitle" -> yourAnswerTitle,
                        "correctAnswerTitle" -> correctAnswerTitle,
                        "correctAnswersTitle" -> correctAnswersTitle,
                        "mediaMarkup" -> mediaMarkup,
                        "responseMarkup" -> responseMarkup)
        val output = engine.layout("src/main/resources/basket.mustache",map)
        val basketFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,basketId + ".html")),"UTF-8")
        basketFile.write(output)
        basketFile.close
      }
    })

  }

  def exportEndOfTestPages(adminLanguages:List[String]) {

    val endOfTestDir = new File(websiteDir,"endoftest")
    if(!endOfTestDir.isDirectory) {
        endOfTestDir.mkdirs()
    }

    for(al <- adminLanguages) { 
        val title = db.getTranslation("Title_LangTestEnd",al)
        val text = db.getTranslation("LangTestEnd_Text",al)
        val nexttooltip = db.getTranslation("Caption_Feedback",al)
        val map = Map("title" -> title,"text" -> text,"nexttooltip" -> nexttooltip,"al" -> al)
        val output = engine.layout("src/main/resources/endoftest.mustache",map)
        val endOfTestFile = new OutputStreamWriter(new FileOutputStream(new File(endOfTestDir,al + ".html")),"UTF-8")
        endOfTestFile.write(output)
        endOfTestFile.close()
    }
  }

  def exportFeedbackMenuPages(adminLanguages:List[String]) {

    val feedbackMenuDir = new File(websiteDir,"feedbackmenu")
    if(!feedbackMenuDir.isDirectory) {
        feedbackMenuDir.mkdirs()
    }

    for(al <- adminLanguages) { 
      val title = db.getTranslation("Title_FeedbackMenu",al)
      val text = db.getTranslation("FeedbackMenu_Text",al)
      val resultsTitle = db.getTranslation("Title_Results",al)
      val yourLevelText = db.getTranslation("FeedbackOption_Level",al)
      val checkAnswersText = db.getTranslation("FeedbackOption_CheckAnswers",al)
      val placementTestText = db.getTranslation("Title_Placement",al)
      val saFeedbackText = db.getTranslation("Title_SelfAssessFeedback",al)
      val adviceTitle = db.getTranslation("Title_Advice",al)
      val adviceText = adviceTitle
      val aboutSAText = db.getTranslation("FeedbackOption_AboutSelfAssess",al)
      val skipbtooltip = db.getTranslation("Caption_ChooseAnotherTest",al)
      val skipftooltip = skipbtooltip
      val map = Map("al" -> al,
                      "title" -> title,
                      "text" -> text,
                      "resultsTitle" -> resultsTitle,
                      "yourLevelText" -> yourLevelText,
                      "checkAnswersText" -> checkAnswersText,
                      "placementTestText" -> placementTestText,
                      "saFeedbackText" -> saFeedbackText,
                      "adviceTitle" -> adviceTitle,
                      "adviceText" -> adviceText,
                      "aboutSAText" -> aboutSAText,
                      "skipbtooltip" -> skipbtooltip,
                      "skipftooltip" -> skipftooltip)
      val output = engine.layout("src/main/resources/feedbackmenu.mustache",map)
      val feedbackMenuFile = new OutputStreamWriter(new FileOutputStream(new File(feedbackMenuDir,al + ".html")),"UTF-8")
      feedbackMenuFile.write(output)
      feedbackMenuFile.close
    }
  }

  def exportSAFeedbackPages(adminLanguages:List[String]) {

    val saFeedbackDir = new File(websiteDir,"safeedback")
    if(!saFeedbackDir.isDirectory) {
        saFeedbackDir.mkdirs()
    }

    val levels = db.getItemLevels

    for(al <- adminLanguages) { 
      val alDir = new File(saFeedbackDir,al)
      if(!alDir.isDirectory) {
        alDir.mkdir()
      }

      val title = db.getTranslation("Title_SelfAssessFeedback",al)
      val prevtooltip = db.getTranslation("Caption_BacktoFeedback",al)
      val aboutSAText = db.getTranslation("FeedbackOption_AboutSelfAssess",al)
      val overEst = db.getTranslation("SelfAssessFeedback_OverEst_Par2",al)
      val underEst = db.getTranslation("SelfAssessFeedback_UnderEst_Par2",al)

      levels.foreach(itemLevel => {
        val itemLevelDir = new File(alDir,itemLevel)
        if(!itemLevelDir.isDirectory) {
          itemLevelDir.mkdir()
        }
        levels.foreach(saLevel => {
          val partOne = db.getTranslationLike("SelfAssessFeedback%Par1#" + itemLevel + "#" + saLevel,al)
          val partTwo = {
              if(saLevel > itemLevel) {
                overEst
              } else {
                underEst
              }
            }

          val map = Map("al" -> al,
                      "title" -> title,
                      "partOne" -> partOne,
                      "partTwo" -> partTwo,
                      "aboutSAText" -> aboutSAText,
                      "prevtooltip" -> prevtooltip)
          val output = engine.layout("src/main/resources/safeedback.mustache",map)
          val saFeedbackFile = new OutputStreamWriter(new FileOutputStream(new File(itemLevelDir,saLevel + ".html")),"UTF-8")
          saFeedbackFile.write(output)
          saFeedbackFile.close
        })
      })
    }
  }

  def exportTestResultPages(adminLanguages:List[String]) {

    val testresultsDir = new File(websiteDir,"testresults")
    if(!testresultsDir.isDirectory) {
        testresultsDir.mkdirs()
    }

    val levels = db.getItemLevels

    for(al <- adminLanguages) { 

      val alDir = new File(testresultsDir,al)
      if(!alDir.isDirectory) {
        alDir.mkdir()
      }

      val title = db.getTranslation("Title_DIALANGTestResults",al)
      val prevtooltip = db.getTranslation("Caption_BacktoWelcome",al)

      for(skill <- db.saSkills) {

        val skillDir = new File(alDir,skill.toLowerCase)
        if(!skillDir.isDirectory) {
          skillDir.mkdir()
        }

        val explanTexts = levels.map(l => {
            val text = db.getTranslation("TestResults_Text#" + skill + "#" + l,al)
            ((l + "Explanation",text))
          })

        levels.foreach(itemLevel => {
          val text = db.getTranslation("TestResults_Text#" + skill + "#" + itemLevel,al)
          val map = Map("al" -> al,
                      "title" -> title,
                      "text" -> text,
                      "itemLevel" -> itemLevel,
                      "prevtooltip" -> prevtooltip) ++ explanTexts
          val output = engine.layout("src/main/resources/testresults.mustache",map)
          val testresultsFile = new OutputStreamWriter(new FileOutputStream(new File(skillDir,itemLevel + ".html")),"UTF-8")
          testresultsFile.write(output)
          testresultsFile.close()
        })
      }
    }
  }

  def exportItemReviewPages(adminLanguages:List[String]) {

    val itemreviewDir = new File(websiteDir,"itemreview")
    if(!itemreviewDir.isDirectory) {
        itemreviewDir.mkdirs()
    }

    for(al <- adminLanguages) { 

      val title = db.getTranslation("Title_ItemReview",al)
      val text = db.getTranslation("ItemReview_Text",al)
      val prevtooltip = db.getTranslation("Caption_BacktoFeedback",al)
      val subskills = {
          val tmp = new ListBuffer[Map[String,String]]
          db.getSubSkills(al).foreach(t => {
              tmp += Map("code" -> t._1,"description" -> t._2)
          })
          tmp.toList
        }
      val map = Map("title" -> title,"text" -> text,"prevtooltip" -> prevtooltip,"subskills" -> subskills)
      val output = engine.layout("src/main/resources/itemreviewwrapper.mustache",map)
      val itemreviewFile = new OutputStreamWriter(new FileOutputStream(new File(itemreviewDir,al + ".html")),"UTF-8")
      itemreviewFile.write(output)
      itemreviewFile.close()
    }
  }
}
