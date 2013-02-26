package org.dialang.exporter

import org.fusesource.scalate._

import org.dialang.exporter.db.DB

import java.io.{File,FileOutputStream,OutputStreamWriter}

import scala.collection.JavaConversions._
import scala.collection.mutable.{ListBuffer,HashMap,ArrayBuffer}

object DialangExporter extends App {

  Console.setOut(System.out)

  val db = new DB
  val engine = new TemplateEngine

  val adminLanguages = db.getAdminLanguageLocales

  exportAls
  exportLegendPages(adminLanguages)
  exportFlowchartPages(adminLanguages)
  exportTLSPages(adminLanguages)
  exportVSPTIntroPages(adminLanguages)
  exportVSPTPages(adminLanguages)
  exportVSPTFeedbackPages(adminLanguages)
  exportSAIntroPages(adminLanguages)
  exportSAPages(adminLanguages)
  exportTestIntroPages(adminLanguages)

  sys.exit

  def exportAls {
    val output = engine.layout("src/main/resources/als.mustache",db.getAdminLanguages)
    val alsFile = new OutputStreamWriter(new FileOutputStream("website/dialang/content/als.html"),"UTF-8")
    alsFile.write(output)
    alsFile.close
  }

  def exportLegendPages(adminLanguages:List[String]) {

    val legendDir = new File("website/dialang/content/legend")
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
        legendFile.close
    }
  }

  def exportFlowchartPages(adminLanguages:List[String]) {

    val flowchartDir = new File("website/dialang/content/flowchart")
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

    val tlsDir = new File("website/dialang/content/tls")
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

    val vsptIntroDir = new File("website/dialang/content/vsptintro")
    if(!vsptIntroDir.isDirectory) vsptIntroDir.mkdirs()

    val testLanguages = db.getTestLanguageCodes

    for(al <- adminLanguages) { 
      val prevtooltip = db.getTranslation("Caption_BacktoChooseTest",al)
      val nexttooltip = db.getTranslation("Caption_StartPlacement",al)
      val skipftooltip = db.getTranslation("Caption_SkipPlacement",al)
      val title = db.getTranslation("Title_Placement",al)
      val text = db.getTranslation("PlacementIntro_Text",al)
      val map = Map("al" -> al,
                  "title" -> title,
                  "text" -> text,
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
    val vsptDir = new File("website/dialang/content/vspt")
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
    val vsptfeedbackDir = new File("website/dialang/content/vsptfeedback")
    val levels = db.vsptLevels

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

    val saIntroDir = new File("website/dialang/content/saintro")

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
        val map = Map("al" -> al,
                    //"tl" -> tl,
                    "skill" -> skill.toLowerCase,
                    "title" -> title,
                    "text" -> text,
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

    val saDir = new File("website/dialang/content/sa")

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

      for(skill <- db.saSkills) {
        val statements = db.getSAStatements(al,skill.toLowerCase)

        val title = db.getTranslation("Title_SelfAssess#" + skill,al)
        val map = Map("al" -> al,
                    "title" -> title,
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

    val testIntroDir = new File("website/dialang/content/testintro")
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
      val map = Map("al" -> al,
                  "title" -> title,
                  "text" -> text,
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

  def exportMCQBasketPages(adminLanguages:List[String]) {

    val basketDir = new File("website/dialang/content/baskets")
    if(!basketDir.isDirectory) {
        basketDir.mkdirs()
    }
  }
}
