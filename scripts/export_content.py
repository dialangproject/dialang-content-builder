import pystache
import psycopg2
import datetime
import os
import configparser
from pathlib import Path

start = datetime.datetime.now()

conn = psycopg2.connect(
    database="DIALANG",
    user="dialangadmin",
    host="localhost",  # Usually 'localhost'
    port="5432")

cursor = conn.cursor()
cursor.execute("SELECT * FROM admin_languages")
rows = list(cursor.fetchall())
admin_languages = [{ 'locale': r[0], 'description': r[1] } for r in rows]
cursor.close()

cursor = conn.cursor()
cursor.execute("SELECT locale,two_letter_code FROM test_languages")
rows = list(cursor.fetchall())
test_languages = [{ 'locale': r[0], 'two_letter_code': r[1] } for r in rows]
cursor.close()

base_dir = '../../dialang-web/static-site/content'

translations = {}

for language in admin_languages:
    al = language["locale"]
    config = configparser.ConfigParser()
    config.read('../admin-texts/admintexts_' + al + '.properties')
    translations[al] = config._sections['AdminTexts']

def export_als():
    renderer = pystache.Renderer()
    funder_message = 'The original DIALANG Project was carried out with the support of the commission of the European Communities within the framework of the SOCRATES programme, LINGUA 2'

    als_fragment = renderer.render_path('../templates/als.mustache', { 'languages': admin_languages, 'fundermessage': funder_message, 'stage': 'prod' })
    als_file = renderer.render_path('../templates/shell.mustache', { 'state': 'als', 'content': als_fragment })
    with open(base_dir + '/als.html', 'w') as f:
        print(als_file, file = f)

def export_help_dialogs():

    Path(base_dir + '/help').mkdir(exist_ok=True)

    for al in [al['locale'] for al in admin_languages]:
        key = translations[al]['title_key']
        next = translations[al]['caption_continuenext']
        back = translations[al]['caption_backprevious']
        skipf = translations[al]['caption_skipnextsection']
        skipb = translations[al]['caption_skipprevioussection']
        yes = translations[al]['caption_yes']
        no = translations[al]['caption_no']
        help = translations[al]['caption_help']
        smiley = translations[al]['captioninstantonoff']
        keyboard = translations[al]['caption_additionalcharacters']
        speaker = translations[al]['caption_playsound']
        aboutTitle = translations[al]['title_aboutdialang']
        crDialang = translations[al]['bits_copyrightdialang']
        crLancaster = translations[al]['bits_copyrightlancaster']
        vsptTitle = translations[al]['title_placement']
        vsptText = translations[al]['help_texts_placement']
        saTitle = translations[al]['title_selfassess']
        saText = translations[al]['help_texts_selfassess']

        values = {
            "al": al,
            "key": key,
            "next": next,
            "back": back,
            "skipf": skipf,
            "skipb": skipb,
            "yes": yes,
            "no": no,
            "help": help,
            "smiley": smiley,
            "keyboard": keyboard,
            "speaker": speaker,
            "aboutTitle": aboutTitle,
            "crDialang": crDialang,
            "crLancaster": crLancaster,
            "vsptTitle": vsptTitle,
            "vsptText": vsptText,
            "saTitle": saTitle,
            "saText": saText
        }

        renderer = pystache.Renderer()
        help_fragment = renderer.render_path('../templates/helpdialog.mustache', values)
        with open(base_dir + '/help/' + al + '.html', 'w') as f:
            print(help_fragment, file = f)

def export_legend():

    Path(base_dir + '/legend').mkdir(exist_ok=True)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin_languages")

    for al in [al['locale'] for al in admin_languages]:
        key = translations[al]['title_key']

        welcome = translations[al]['title_welcomedialang']
        next = translations[al]['caption_continuenext']
        back = translations[al]['caption_backprevious']
        skipf = translations[al]['caption_skipnextsection']
        skipb = translations[al]['caption_skipprevioussection']
        yes = translations[al]['caption_yes']
        no = translations[al]['caption_no']
        help = translations[al]['caption_help']
        smiley = translations[al]['captioninstantonoff']
        keyboard = translations[al]['caption_additionalcharacters']
        speaker = translations[al]['caption_playsound']
        backtooltip = translations[al]['caption_backtoals']
        nexttooltip = translations[al]['caption_continuenext']
        values = {
            "key": key,
            "next": next,
            "back": back,
            "welcome": welcome,
            "skipf": skipf,
            "skipb": skipb,
            "yes": yes,
            "no": no,
            "help": help,
            "smiley": smiley,
            "keyboard": keyboard,
            "speaker": speaker,
            "backtooltip": backtooltip,
            "nexttooltip": nexttooltip,
            "al": al,
            "stage": "prod"
        }

        renderer = pystache.Renderer()
        legend_fragment = renderer.render_path('../templates/legend.mustache', values)
        with open(base_dir + '/legend/' + al + '.html', 'w') as f:
            print(legend_fragment, file = f)

        tip_output = renderer.render_path('../templates/toolbartooltips.mustache', values)
        with open(base_dir + '/legend/' + al + '-toolbarTooltips.json', 'w') as f:
            print(tip_output, file = f)

def export_flowchart():

    Path(base_dir + '/flowchart').mkdir(exist_ok=True)

    for al in [al['locale'] for al in admin_languages]:
        welcomeTitle = translations[al]['title_welcomedialang']
        welcomeText = translations[al]['welcome_intro_text']
        procedureTitle = translations[al]['title_procedurecaps']
        procedureText = translations[al]['welcome_procedure_text']
        backtooltip = translations[al]['caption_backtowelcome']
        nexttooltip = translations[al]['caption_gotochoosetest']
        stage1Title = translations[al]['title_choosetest']
        stage1 = translations[al]['welcome_chart_choosetest_text']
        stage2Title = translations[al]['title_placement']
        stage2 = translations[al]['welcome_chart_placement_text']
        stage3Title = translations[al]['title_selfassess']
        stage3 = translations[al]['welcome_chart_selfassess_text']
        stage4Title = translations[al]['title_langtest']
        stage4 = translations[al]['welcome_chart_langtest_text']
        stage5Title = translations[al]['title_feedbackresultsadvice']
        stage5 = translations[al]['welcome_chart_feedback_text']

        values = {
            "al": al,
            "welcomeTitle": welcomeTitle,
            "welcomeText": welcomeText,
            "procedureTitle": procedureTitle,
            "procedureText": procedureText,
            "stage1Title": stage1Title,
            "stage1": stage1,
            "stage2Title": stage2Title,
            "stage2": stage2,
            "stage3Title": stage3Title,
            "stage3": stage3,
            "stage4Title": stage4Title,
            "stage4": stage4,
            "stage5Title": stage5Title,
            "stage5": stage5,
            "backtooltip": backtooltip,
            "nexttooltip": nexttooltip,
            "stage": "prod"
        }

        renderer = pystache.Renderer()
        flowchart_fragment = renderer.render_path('../templates/flowchart.mustache', values)
        with open(base_dir + '/flowchart/' + al + '.html', 'w') as f:
            print(flowchart_fragment, file = f)

        tip_output = renderer.render_path('../templates/toolbartooltips.mustache', values)
        with open(base_dir + '/flowchart/' + al + '-toolbarTooltips.json', 'w') as f:
            print(tip_output, file = f)

def export_tls():

    Path(base_dir + '/tls').mkdir(exist_ok=True)

    for al in [al['locale'] for al in admin_languages]:

        skipbacktooltip = translations[al]['caption_backtoals']
        backtooltip = translations[al]['caption_backtowelcome']
        tlsTitle = translations[al]['title_choosetest']
        listeningTooltip = translations[al]['choosetest_skill#listening']
        writingTooltip = translations[al]['choosetest_skill#writing']
        readingTooltip = translations[al]['choosetest_skill#reading']
        structuresTooltip = translations[al]['choosetest_skill#structures']
        vocabularyTooltip = translations[al]['choosetest_skill#vocabulary']

        # For the disclaimer dialog box
        disclaimerTitle = translations[al]['title_usemisuse']
        disclaimer = translations[al]['disclaimer_usemisuse']

        # For the test confirmation dialog box
        testChosen = translations[al]['dialogues_testselected']
        yes = translations[al]['caption_yes']
        no = translations[al]['caption_no']

        ok = translations[al]['caption_ok']
        done = translations[al]['caption_done']
        available = translations[al]['caption_available']
        notavailable = translations[al]['caption_notavailable']
        #tls_map = { k.split('#')[1]: v for k, v in translations[al].items() if k.startswith("choosetest_language") }
        test_rows = [{ "languageCode": k.split('#')[1], "languageName": v } for k, v in translations[al].items() if k.startswith("choosetest_language") ]

        values = {
            "al": al,
            "tlsTitle": tlsTitle,
            "testrows": test_rows,
            "skipbacktooltip": skipbacktooltip,
            "backtooltip": backtooltip,
            "listeningTooltip": listeningTooltip,
            "writingTooltip": writingTooltip,
            "disclaimerTitle": disclaimerTitle,
            "disclaimer": disclaimer,
            "testChosen": testChosen,
            "yes": yes,
            "no": no,
            "ok": ok,
            "done": done,
            "available": available,
            "notavailable": notavailable,
            "readingTooltip": readingTooltip,
            "structuresTooltip": structuresTooltip,
            "vocabularyTooltip": vocabularyTooltip,
            "stage": "prod"
        }

        renderer = pystache.Renderer()
        tls_fragment = renderer.render_path('../templates/tls.mustache', values)
        with open(base_dir + '/tls/' + al + '.html', 'w') as f:
            print(tls_fragment, file = f)

        tip_output = renderer.render_path('../templates/toolbartooltips.mustache', values)
        with open(base_dir + '/tls/' + al + '-toolbarTooltips.json', 'w') as f:
            print(tip_output, file = f)

def export_vsptintro():

    Path(base_dir + '/vsptintro').mkdir(exist_ok=True)

    for al in [al['locale'] for al in admin_languages]:
        backtooltip = translations[al]['caption_backtochoosetest']
        nexttooltip = translations[al]['caption_startplacement']
        skipforwardtooltip = translations[al]['caption_skipplacement']
        title = translations[al]['title_placement']
        text = translations[al]['placementintro_text']

        # Confirmation dialog texts.
        warningText = translations[al]['dialogues_skipplacement']
        yes = translations[al]['caption_yes']
        no = translations[al]['caption_no']

        values = {
            "al": al,
            "title": title,
            "text": text,
            "warningText": warningText,
            "yes": yes,
            "no": no,
            "nexttooltip": nexttooltip,
            "backtooltip": backtooltip,
            "skipforwardtooltip": skipforwardtooltip
        }

        renderer = pystache.Renderer()
        vsptintro_fragment = renderer.render_path('../templates/vsptintro.mustache', values)
        with open(base_dir + '/vsptintro/' + al + '.html', 'w') as f:
            print(vsptintro_fragment, file = f)

        tip_output = renderer.render_path('../templates/toolbartooltips.mustache', values)
        with open(base_dir + '/vsptintro/' + al + '-toolbarTooltips.json', 'w') as f:
            print(tip_output, file = f)

def export_vspt():

    Path(base_dir + '/vspt').mkdir(exist_ok=True)

    """
    val testLanguagesAndVSPT: Map[String, List[(String,String,Boolean)]]
      = (db.getTestLanguageCodes.foldLeft(
        Map.newBuilder[String, List[(String,String,Boolean)]])
          ((acc,tl) => acc += ((tl._1, db.getVSPTWords(tl._1))))).result()
    """

    test_languages_and_vspt = {}
    for tl in [tl['locale'] for tl in test_languages]:
        cursor = conn.cursor()
        cursor.execute("SELECT word,words.word_id AS id,valid FROM vsp_test_word,words WHERE locale = '" + tl + "' AND vsp_test_word.word_id = words.word_id")
        rows = list(cursor.fetchall())
        vspt_words = [(r[0], r[1], r[2]) for r in rows]
        cursor.close()
        test_languages_and_vspt[tl] = vspt_words

    for al in [al['locale'] for al in admin_languages]:
        Path(base_dir + '/vspt/' + al).mkdir(exist_ok=True)

        title = translations[al]['title_placement']
        submit = translations[al]['caption_submitanswers']
        yes = translations[al]['caption_yes']
        no = translations[al]['caption_no']
        confirmSend = translations[al]['dialogues_submit']
        skipforwardtooltip = translations[al]['caption_quitplacement']

        renderer = pystache.Renderer()
        tip_values = { "nexttooltip": submit, "skipforwardtooltip": skipforwardtooltip }
        tip_output = renderer.render_path('../templates/toolbartooltips.mustache', tip_values)
        with open(base_dir + '/vspt/' + al + '-toolbarTooltips.json', 'w') as f:
            print(tip_output, file = f)

        warning_text = translations[al]['dialogues_skipplacement']

        for tl, word_list in test_languages_and_vspt.items():

            tab_list = []
            words = []

            valid_map = {}

            wi = iter(word_list)

            word_tuple = next(wi, None)

            while word_tuple is not None:

                word_1 = word_tuple[0]
                id_1 = word_tuple[1]
                valid_map[id_1] = word_tuple[2]
                valid_class_1 = "correct" if word_tuple[2] else "incorrect"
                invalid_class_1 = "incorrect" if word_tuple[2] else "correct"
                words.append({"id": id_1})

                word_tuple = next(wi, None)
                if word_tuple is None:
                    break
                word_2 = word_tuple[0]
                id_2 = word_tuple[1]
                valid_class_2 = "correct" if word_tuple[2] else "incorrect"
                invalid_class_2 = "incorrect" if word_tuple[2] else "correct"
                valid_2 = word_tuple[2]
                words.append({"id": id_2})

                word_tuple = next(wi, None)
                if word_tuple is None:
                    break
                word_3 = word_tuple[0]
                id_3 = word_tuple[1]
                valid_class_3 = "correct" if word_tuple[2] else "incorrect"
                invalid_class_3 = "incorrect" if word_tuple[2] else "correct"
                valid_3 = word_tuple[2]
                words.append({"id": id_3})

                tab_list.append({
                    "word1": word_1,
                    "id1": id_1,
                    "valid_class_1": valid_class_1,
                    "invalid_class_1": invalid_class_1,
                    "word2": word_2,
                    "id2": id_2,
                    "valid_class_2": valid_class_2,
                    "invalid_class_2": invalid_class_2,
                    "valid2": valid_2,
                    "word3": word_3,
                    "id3": id_3,
                    "valid_class_3": valid_class_3,
                    "invalid_class_3": invalid_class_3
                })

            #print(tab_list)

            def is_correct_function(compound_id):
                print("COMPOUND ID: " + compound_id)
                word_id, validity = compound_id.split("_")
                print("WORD ID: " + word_id)
                if valid_map[word_id]:
                    return "correct" if validity == "valid" else "incorrect"
                else:
                    return "correct" if validity == "invalid" else "incorrect"

            values = {
                "al": al,
                "title": title,
                #"isCorrect": is_correct_function,
                "tl": tl,
                "warningText": warning_text,
                "yes": yes,
                "no": no,
                "confirmsendquestion": confirmSend,
                "submit": submit,
                "words": words,
                "tab": tab_list
            }

            renderer = pystache.Renderer()
            vspt_fragment = renderer.render_path('../templates/vspt.mustache', values)
            with open(base_dir + '/vspt/' + al + '/' + tl + '.html', 'w') as f:
                print(vspt_fragment, file = f)

"""
export_als()
export_help_dialogs()
export_legend()
export_flowchart()
export_tls()
export_vsptintro()
"""
export_vspt()

"""
  val db = new DB
  val engine = new TemplateEngine
  val websiteDir = new File(args(0))

  if (!websiteDir.exists) {
    websiteDir.mkdirs();
  }

  val adminLanguages = db.getAdminLanguageLocales
  val adminLocalesST= conn.prepareStatement("SELECT locale FROM admin_languages")

  exportAls()
  exportHelpDialogs(adminLanguages)
  exportLegendPages(adminLanguages)
  exportFlowchartPages(adminLanguages)
  exportTLSPages(adminLanguages)
  exportVSPTIntroPages(adminLanguages)
  exportVSPTPages(adminLanguages)
  exportVSPTFeedbackPages(adminLanguages)
  exportSAIntroPages(adminLanguages)
  exportSAPages(adminLanguages)
  exportKeyboardFragments()
  exportTestIntroPages(adminLanguages)
  exportBasketPages(adminLanguages)
  exportEndOfTestPages(adminLanguages)
  exportFeedbackMenuPages(adminLanguages)
  exportSAFeedbackPages(adminLanguages)
  exportTestResultPages(adminLanguages)
  exportItemReviewPages(adminLanguages)
  exportExplfbPages(adminLanguages)
  exportAdvfbPages(adminLanguages)

  db.cleanup()

  val end = (new Date).getTime

  val elapsed = end - start

  println("Export took " + elapsed/1000L + " seconds")

  sys.exit()

  def exportAls(): Unit = {
    
    val listOutput = engine.layout("src/main/resources/als.mustache", db.getAdminLanguages)
    val output = engine.layout("src/main/resources/shell.mustache", Map("state" -> "als", "content" -> listOutput))
    val alsFile = new OutputStreamWriter(new FileOutputStream(new File(websiteDir, "als.html")), "UTF-8")
    alsFile.write(output)
    alsFile.close()
  }

  def exportHelpDialogs(adminLanguages: List[String]): Unit = {

    val helpDir = new File(websiteDir, "help")
    if (!helpDir.isDirectory) helpDir.mkdirs()

    for (al <- adminLanguages) { 
      val key = db.getTranslation("Title_Key", al)
      val next = db.getTranslation("Caption_ContinueNext", al)
      val back = db.getTranslation("Caption_BackPrevious", al)
      val skipf = db.getTranslation("Caption_SkipNextSection", al)
      val skipb = db.getTranslation("Caption_SkipPreviousSection", al)
      val yes = db.getTranslation("Caption_Yes", al)
      val no = db.getTranslation("Caption_No", al)
      val help = db.getTranslation("Caption_Help", al)
      val smiley = db.getTranslation("CaptionInstantOnOff",al)
      val keyboard = db.getTranslation("Caption_AdditionalCharacters",al)
      val speaker = db.getTranslation("Caption_PlaySound",al)
      val aboutTitle = db.getTranslation("Title_AboutDIALANG",al)
      val crDialang = db.getTranslation("Bits_CopyrightDIALANG",al)
      val crLancaster = db.getTranslation("Bits_CopyrightLancaster",al)
      val vsptTitle = db.getTranslation("Title_Placement",al)
      val vsptText = db.getTranslation("Help_Texts_Placement",al)
      val saTitle = db.getTranslation("Title_SelfAssess",al)
      val saText = db.getTranslation("Help_Texts_SelfAssess",al)
      val map = Map("key" -> key,
                      "next" -> next,
                      "back" -> back,
                      "skipf" -> skipf,
                      "skipb" -> skipb,
                      "yes" -> yes,
                      "no" -> no,
                      "help" -> help,
                      "smiley" -> smiley,
                      "keyboard" -> keyboard,
                      "speaker" -> speaker,
                      "aboutTitle" -> aboutTitle,
                      "crDialang" -> crDialang,
                      "crLancaster" -> crLancaster,
                      "vsptTitle" -> vsptTitle,
                      "vsptText" -> vsptText,
                      "saTitle" -> saTitle,
                      "saText" -> saText)

      val output = engine.layout("src/main/resources/helpdialog.mustache",map)
      val helpFile = new OutputStreamWriter(new FileOutputStream(new File(helpDir,al + ".html")),"UTF-8")
      helpFile.write(output)
      helpFile.close
    }
  }

  def exportLegendPages(adminLanguages: List[String]): Unit = {

    val legendDir = new File(websiteDir,"legend")
    if (!legendDir.isDirectory) {
        legendDir.mkdirs()
    }

    for (al <- adminLanguages) { 
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
      val backtooltip = db.getTranslation("Caption_BacktoALS",al)
      val nexttooltip = db.getTranslation("Caption_ContinueNext",al)
      val map = Map("key" -> key,
                      "next" -> next,
                      "back" -> back,
                      "welcome" -> welcome,
                      "skipf" -> skipf,
                      "skipb" -> skipb,
                      "yes" -> yes,
                      "no" -> no,
                      "help" -> help,
                      "smiley" -> smiley,
                      "keyboard" -> keyboard,
                      "speaker" -> speaker,
                      "backtooltip" -> backtooltip,
                      "nexttooltip" -> nexttooltip,
                      "al" -> al)

      val output = engine.layout("src/main/resources/legend.mustache",map)
      val legendFile = new OutputStreamWriter(new FileOutputStream(new File(legendDir,al + ".html")),"UTF-8")
      legendFile.write(output)
      legendFile.close()

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",map)
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(legendDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()
    }
  }

  def exportFlowchartPages(adminLanguages: List[String]): Unit = {

    val flowchartDir = new File(websiteDir,"flowchart")
    if (!flowchartDir.isDirectory) {
        flowchartDir.mkdirs()
    }

    for (al <- adminLanguages) { 
      val welcomeTitle = db.getTranslation("Title_WelcomeDIALANG",al)
      val welcomeText = db.getTranslation("Welcome_Intro_Text",al)
      val procedureTitle = db.getTranslation("Title_ProcedureCAPS",al)
      val procedureText = db.getTranslation("Welcome_Procedure_Text",al)
      val backtooltip = db.getTranslation("Caption_BacktoWelcome",al)
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
                      "backtooltip" -> backtooltip,
                      "nexttooltip" -> nexttooltip )

      val output = engine.layout("src/main/resources/flowchart.mustache",map)
      val flowchartFile = new OutputStreamWriter(new FileOutputStream(new File(flowchartDir,al + ".html")),"UTF-8")
      flowchartFile.write(output)
      flowchartFile.close

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",map)
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(flowchartDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()
    }
  }

  def exportTLSPages(adminLanguages: List[String]): Unit = {

    val tlsDir = new File(websiteDir,"tls")
    if (!tlsDir.isDirectory) {
        tlsDir.mkdirs()
    }

    for (al <- adminLanguages) { 
      val skipbacktooltip = db.getTranslation("Caption_BacktoALS",al)
      val backtooltip = db.getTranslation("Caption_BacktoWelcome",al)
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
      tlsMap.zipWithIndex.foreach(t => {
        if (t._2 < (tlsMap.size - 2)) {
            testRows += Map("languageName" -> t._1._2,"languageCode" -> t._1._1)
        } else {
            testRows += Map("languageName" -> t._1._2,"languageCode" -> t._1._1,"last" -> "true")
        }
      })

      val map = Map("al" -> al,
                      "tlsTitle" -> tlsTitle,
                      "testrows" -> testRows.toList,
                      "skipbacktooltip" -> skipbacktooltip,
                      "backtooltip" -> backtooltip,
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

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",map)
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(tlsDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()
    }
  }

  def exportVSPTIntroPages(adminLanguages: List[String]): Unit = {

    val vsptIntroDir = new File(websiteDir,"vsptintro")
    if (!vsptIntroDir.isDirectory) vsptIntroDir.mkdirs()

    val testLanguages = db.getTestLanguageCodes

    for (al <- adminLanguages) { 
      val backtooltip = db.getTranslation("Caption_BacktoChooseTest",al)
      val nexttooltip = db.getTranslation("Caption_StartPlacement",al)
      val skipforwardtooltip = db.getTranslation("Caption_SkipPlacement",al)
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
                  "backtooltip" -> backtooltip,
                  "skipforwardtooltip" -> skipforwardtooltip )
      val output = engine.layout("src/main/resources/vsptintro.mustache",map)
      val vsptIntroFile = new OutputStreamWriter(new FileOutputStream(new File(vsptIntroDir,al + ".html")),"UTF-8")
      vsptIntroFile.write(output)
      vsptIntroFile.close

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",map)
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(vsptIntroDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()
    }
  }

  def exportVSPTPages(adminLanguages: List[String]): Unit = {

    val vsptDir = new File(websiteDir,"vspt")

    val testLanguagesAndVSPT: Map[String, List[(String,String,Boolean)]]
      = (db.getTestLanguageCodes.foldLeft(
        Map.newBuilder[String, List[(String,String,Boolean)]])
          ((acc,tl) => acc += ((tl._1, db.getVSPTWords(tl._1))))).result()

    for (al <- adminLanguages) { 
      val alDir = new File(vsptDir,al)
      if (!alDir.isDirectory) {
        alDir.mkdirs()
      }

      val title = db.getTranslation("Title_Placement",al)
      val submit = db.getTranslation("Caption_SubmitAnswers",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)
      val confirmSend = db.getTranslation("Dialogues_Submit",al)
      val skipforwardtooltip = db.getTranslation("Caption_QuitPlacement",al)

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("nexttooltip" -> submit,"skipforwardtooltip" -> skipforwardtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(vsptDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()

      // Confirmation dialog texts.
      val warningText = db.getTranslation("Dialogues_SkipPlacement",al)

      for (tl <- testLanguagesAndVSPT) { 
        val wordList = tl._2

        val tabList = new ListBuffer[Map[String,String]]
        val words = new ListBuffer[Map[String,String]]

        val validMap = new HashMap[String,Boolean]

        val wi = wordList.iterator
        while(wi.hasNext) {
          var wordTuple = wi.next()
          val word1 = wordTuple._1
          val id1 = wordTuple._2
          validMap += (id1 -> wordTuple._3)
          words += Map("id" -> id1)

          wordTuple = wi.next()
          val word2 = wordTuple._1
          val id2 = wordTuple._2
          validMap += (id2 -> wordTuple._3)
          words += Map("id" -> id2)

          wordTuple = wi.next()
          val word3 = wordTuple._1
          val id3 = wordTuple._2
          validMap += (id3 -> wordTuple._3)
          words += Map("id" -> id3)

          tabList += Map("word1" -> word1,"id1" -> id1,
                "word2" -> word2,"id2" -> id2,
                "word3" -> word3,"id3" -> id3)
        }

        val map = Map( "al" -> al,
                        "title" -> title,
                        "isCorrect" -> ((compoundId:String) => {
                            val parts = compoundId.split("_")
                            val id = parts(0)
                            val response = parts(1)
                            if (validMap.get(id).get) {
                              if (response == "valid") {
                                "correct"
                              } else {
                                "incorrect"
                              }
                            } else {
                              if (response == "invalid") {
                                "correct"
                              } else {
                                "incorrect"
                              }
                            }
                          }),
                        "tl" -> tl,
                        "warningText" -> warningText,
                        "yes" -> yes,
                        "no" -> no,
                        "confirmsendquestion" -> confirmSend,
                        "submit" -> submit,
                        "words" -> words,
                        "tab" -> tabList.toList )
        val output = engine.layout("src/main/resources/vspt.mustache",map)
        val vsptFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,tl._1 + ".html")),"UTF-8")
        vsptFile.write(output)
        vsptFile.close
      }
    }
  }

  def exportVSPTFeedbackPages(adminLanguages: List[String]): Unit = {

    val vsptFeedbackDir = new File(websiteDir, "vsptfeedback")
    if (!vsptFeedbackDir.isDirectory) {
      vsptFeedbackDir.mkdir()
    }

    val levels = db.getVSPLevels

    for (al <- adminLanguages) { 
      val title = db.getTranslation("Title_PlacementFeedback", al)
      val yourscore = db.getTranslation("PlacementFeedback_YourScore", al)
      val backtooltip = db.getTranslation("Caption_BacktoFeedback", al)
      val nexttooltip = db.getTranslation("Caption_GotoNext", al)

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache", Map("backtooltip" -> backtooltip, "nexttooltip" -> nexttooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(vsptFeedbackDir, al + "-toolbarTooltips.json")), "UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()

      val levelv6 = db.getTranslation("PlacementFeedback_Text#V6", al)
      val levelv5 = db.getTranslation("PlacementFeedback_Text#V5", al)
      val levelv4 = db.getTranslation("PlacementFeedback_Text#V4", al)
      val levelv3 = db.getTranslation("PlacementFeedback_Text#V3", al)
      val levelv2 = db.getTranslation("PlacementFeedback_Text#V2", al)
      val levelv1 = db.getTranslation("PlacementFeedback_Text#V1", al)

      val map = Map( "al" -> al,
                      "title" -> title,
                      "yourscore" -> yourscore,
                      "levelv6" -> levelv6,
                      "levelv5" -> levelv5,
                      "levelv4" -> levelv4,
                      "levelv3" -> levelv3,
                      "levelv2" -> levelv2,
                      "levelv1" -> levelv1,
                      "nexttooltip" -> nexttooltip)
      val output = engine.layout("src/main/resources/vsptfeedback.mustache", map)
      val vsptfeedbackFile = new OutputStreamWriter(new FileOutputStream(new File(vsptFeedbackDir, al + ".html")),"UTF-8")
      vsptfeedbackFile.write(output)
      vsptfeedbackFile.close
    }
  }

  def exportSAIntroPages(adminLanguages:List[String]): Unit = {

    val saIntroDir = new File(websiteDir,"saintro")

    for (al <- adminLanguages) { 
      val alDir = new File(saIntroDir,al)
      if (!alDir.isDirectory) {
        alDir.mkdirs()
      }

      val nexttooltip = db.getTranslation("Caption_StartSelfAssess",al)
      val skipforwardtooltip = db.getTranslation("Caption_SkipSelfAssess",al)
      val text = db.getTranslation("SelfAssessIntro_Text",al)

      // Confirmation dialog texts.
      val warningText = db.getTranslation("Dialogues_SkipSelfAssess",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("nexttooltip" -> nexttooltip,"skipforwardtooltip" -> skipforwardtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(saIntroDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()

      for (skill <- db.saSkills) {

        val title = db.getTranslation("Title_SelfAssess#" + skill,al)

        val map = Map("al" -> al,
                    "skill" -> skill.toLowerCase,
                    "title" -> title,
                    "text" -> text,
                    "warningText" -> warningText,
                    "yes" -> yes,
                    "no" -> no)
        val output = engine.layout("src/main/resources/saintro.mustache",map)
        val saIntroFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,skill.toLowerCase + ".html")),"UTF-8")
        saIntroFile.write(output)
        saIntroFile.close
      }
    }
  }

  def exportSAPages(adminLanguages: List[String]): Unit = {

    val saDir = new File(websiteDir,"sa")

    for (al <- adminLanguages) { 
      val alDir = new File(saDir,al)
      if (!alDir.isDirectory) {
        alDir.mkdirs()
      }

      val submit = db.getTranslation("Caption_SubmitAnswers",al)
      val skipforwardtooltip = db.getTranslation("Caption_QuitSelfAssess",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)
      val confirmSend = db.getTranslation("Dialogues_Submit",al)

      // Confirmation dialog texts.
      val warningText = db.getTranslation("Dialogues_SkipSelfAssess",al)

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("nexttooltip" -> submit,"skipforwardtooltip" -> skipforwardtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(saDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()

      for (skill <- db.saSkills) {
        val statements = db.getSAStatements(al, skill.toLowerCase)

        val title = db.getTranslation("Title_SelfAssess#" + skill,al)
        val map = Map("al" -> al,
                    "title" -> title,
                    "warningText" -> warningText,
                    "submit" -> submit,
                    "yes" -> yes,
                    "no" -> no,
                     "confirmsendquestion" -> confirmSend,
                    "statements" -> statements )
        val output = engine.layout("src/main/resources/sa.mustache",map)
        val saFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,skill.toLowerCase + ".html")),"UTF-8")
        saFile.write(output)
        saFile.close()
      }
    }
  }

  def exportTestIntroPages(adminLanguages: List[String]): Unit = {

    val testIntroDir = new File(websiteDir,"testintro")
    if (!testIntroDir.isDirectory) {
        testIntroDir.mkdirs()
    }

    for (al <- adminLanguages) { 
      val nexttooltip = db.getTranslation("Caption_StartTest",al)
      val skipforwardtooltip = db.getTranslation("Caption_SkipLangTest",al)
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
                  "instantfeedbackofftooltip" -> instantfeedbackofftooltip )
      val output = engine.layout("src/main/resources/testintro.mustache",map)
      val saIntroFile = new OutputStreamWriter(new FileOutputStream(new File(testIntroDir,al + ".html")),"UTF-8")
      saIntroFile.write(output)
      saIntroFile.close

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("nexttooltip" -> nexttooltip,"skipforwardtooltip" -> skipforwardtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(testIntroDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()
    }
  }

  def exportKeyboardFragments(): Unit = {

    val keyboardDir = new File(websiteDir, "keyboards")
    if (!keyboardDir.isDirectory) {
        keyboardDir.mkdirs()
    }

    // Load the special characters file
    val specialCharLists = new Properties
    specialCharLists.load(getClass.getResourceAsStream("/org/dialang/exporter/db/special_chars.properties"))

    for ((locale, csv) <- specialCharLists.asScala) {
      val chars = csv.split(",").map(c => Map("char" -> c))
      val output = engine.layout("src/main/resources/keyboard.mustache", Map("chars" -> chars))
      val writer = new FileWriter(new File(keyboardDir, locale + ".html"))
      writer.write(output)
      writer.close()
    }
  }

  def exportBasketPages(adminLanguages: List[String]): Unit = {

    val typeMap = Map( "gapdrop" -> "GapDrop",
                        "gaptext" -> "GapText",
                        "mcq" -> "MCQ",
                        "shortanswer" -> "ShortAnswer",
                        "tabbedpane" -> "TabbedMCQ" )

    val basketDir = new File(websiteDir, "baskets")
    if (!basketDir.isDirectory) {
        basketDir.mkdirs()
    }

    for (al <- adminLanguages) {
      val nexttooltip = db.getTranslation("Caption_Next", al)
      val skipforwardtooltip = db.getTranslation("Caption_QuitLangTest", al)
      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache", Map("nexttooltip" -> nexttooltip, "skipforwardtooltip" -> skipforwardtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(basketDir, al + "-toolbarTooltips.json")), "UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()
    }

    val itemPlaceholderPattern = Pattern.compile("<(\\d*)>")

    db.getBaskets.foreach(basket => {

      // Render the media markup independently of al
      val (mediaMarkup, rubricMediaType) = basket.mediatype match { 
          case "text/html" => {
            (engine.layout("src/main/resources/textmedia.mustache", Map("markup" -> basket.textmedia)), "Text")
          }
          case "audio/mpeg" => {
            (engine.layout("src/main/resources/audiomedia.mustache", Map("filename" -> basket.filemedia)), "Sound")
          }
          case "image/jpeg" => {
            (engine.layout("src/main/resources/imagemedia.mustache", Map("filename" -> basket.filemedia)), "Image")
          }
          case "none" => {
            ("", "NoMedia")
          }
        }

      val basketType = basket.basketType
      val basketId = basket.id
      val skill = basket.skill
      val basketPrompt = basket.prompt

      val (responseMarkup,numberOfItems) = basketType match {
          case "mcq" => {
            val item = db.getItemsForBasket(basketId).head
            val answers = db.getAnswersForItem(item.id)
            val map = Map("itemtext" -> item.text,"itemId" -> item.id.toString,"positionInBasket" -> item.positionInBasket.toString, "answers" -> answers)
            (engine.layout("src/main/resources/mcqresponse.mustache",map),1)
          }
          case "shortanswer" => {
            val items = db.getItemsForBasket(basketId)
            val itemList = items.map(item => {
                Map("id" -> item.id.toString,"text" -> item.text,"positionInBasket" -> item.positionInBasket.toString)
              })
            (engine.layout("src/main/resources/saresponse.mustache",Map("basketPrompt" -> basketPrompt,"items" -> itemList)),items.length)
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

            (engine.layout("src/main/resources/gtresponse.mustache",Map("basketPrompt" -> basketPrompt,"items" -> items,"markup" -> gapMarkup)),items.length)
          }
          case "gapdrop" => {
            val gapText = basket.gaptext
            var gapMarkup = gapText

            val items = db.getItemsForBasket(basketId).map(i => {
                Map("id" -> i.id.toString,"positionInBasket" -> i.positionInBasket.toString)
              })

            val m = itemPlaceholderPattern.matcher(gapText)

            while (m.find()) {
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

            (engine.layout("src/main/resources/gdresponse.mustache",Map("basketPrompt" -> basketPrompt,"items" -> items,"markup" -> gapMarkup)),items.length)
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
                  Map("basketId" -> childBasketId.toString,
                        "itemId" -> item.id.toString,
                        "itemtext" -> item.text,
                        "positionInBasket" -> childBasket.parentTestletPosition,
                        "answers" -> answers)
              })

            (engine.layout("src/main/resources/tabbedpaneresponse.mustache",Map("childBaskets" -> childBaskets)),childBaskets.length)
          }
          case _ => {
            engine.layout("src/main/resources/mcqresponse.mustache",Map("blah" -> "blah"))
          }
        }

        for (al <- adminLanguages) {

          val alDir = new File(basketDir,al)
          if (!alDir.isDirectory) {
            alDir.mkdirs()
          }

          val rubricText = db.getTranslation("LangTest_Rubric#" + typeMap.get(basketType).get + "#" + rubricMediaType,al)

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
                        "responseMarkup" -> responseMarkup,
                        "numberOfItems" -> numberOfItems)
          val output = engine.layout("src/main/resources/basket.mustache", map)
          val basketFile = new OutputStreamWriter(new FileOutputStream(new File(alDir,s"${basketId}.html")),"UTF-8")
          basketFile.write(output)
          basketFile.close

      } // admin language iterator

    }) // basket iterator
  }

  def exportEndOfTestPages(adminLanguages: List[String]): Unit = {

    val endOfTestDir = new File(websiteDir, "endoftest")
    if (!endOfTestDir.isDirectory) {
        endOfTestDir.mkdirs()
    }

    for (al <- adminLanguages) { 
        val title = db.getTranslation("Title_LangTestEnd", al)
        val text = db.getTranslation("LangTestEnd_Text", al)
        val nexttooltip = db.getTranslation("Caption_Feedback", al)

        val output = engine.layout("src/main/resources/endoftest.mustache",Map("title" -> title,"text" -> text))
        val endOfTestFile = new OutputStreamWriter(new FileOutputStream(new File(endOfTestDir,al + ".html")),"UTF-8")
        endOfTestFile.write(output)
        endOfTestFile.close()

        val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("nexttooltip" -> nexttooltip))
        val tipFile = new OutputStreamWriter(new FileOutputStream(new File(endOfTestDir,al + "-toolbarTooltips.json")),"UTF-8")
        tipFile.write(tipOutput)
        tipFile.close()
    }
  }

  def exportFeedbackMenuPages(adminLanguages: List[String]): Unit = {

    val feedbackMenuDir = new File(websiteDir,"feedbackmenu")
    if (!feedbackMenuDir.isDirectory) {
        feedbackMenuDir.mkdirs()
    }

    for (al <- adminLanguages) { 
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
      val restartText = db.getTranslation("Dialogues_QuitFeedback",al)
      val yes = db.getTranslation("Caption_Yes",al)
      val no = db.getTranslation("Caption_No",al)
      val skipforwardtooltip = db.getTranslation("Caption_ChooseAnotherTest",al)
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
                      "restartText" -> restartText,
                      "yes" -> yes,
                      "no" -> no)
      val output = engine.layout("src/main/resources/feedbackmenu.mustache",map)
      val feedbackMenuFile = new OutputStreamWriter(new FileOutputStream(new File(feedbackMenuDir,al + ".html")),"UTF-8")
      feedbackMenuFile.write(output)
      feedbackMenuFile.close

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("skipbacktooltip" -> "","skipforwardtooltip" -> skipforwardtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(feedbackMenuDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()
    }
  }

  def exportSAFeedbackPages(adminLanguages: List[String]): Unit = {

    val saFeedbackDir = new File(websiteDir,"safeedback")
    if (!saFeedbackDir.isDirectory) {
        saFeedbackDir.mkdirs()
    }

    val levels = db.getItemLevels

    for (al <- adminLanguages) { 
      val alDir = new File(saFeedbackDir,al)
      if (!alDir.isDirectory) {
        alDir.mkdir()
      }

      val backtooltip = db.getTranslation("Caption_BacktoFeedback",al)

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("backtooltip" -> backtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(saFeedbackDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()

      val title = db.getTranslation("Title_SelfAssessFeedback",al)
      val aboutSAText = db.getTranslation("FeedbackOption_AboutSelfAssess",al)
      val overEst = db.getTranslation("SelfAssessFeedback_OverEst_Par2",al)
      val accurate = db.getTranslation("SelfAssessFeedback_Match_Par2",al)
      val underEst = db.getTranslation("SelfAssessFeedback_UnderEst_Par2",al)

      for (itemLevel <- levels) {
        val itemLevelDir = new File(alDir,itemLevel)
        if (!itemLevelDir.isDirectory) {
          itemLevelDir.mkdir()
        }
        for (saLevel <- levels) {
          val partOne = {
              if (saLevel != itemLevel) {
                db.getTranslationLike("SelfAssessFeedback%Par1#" + itemLevel + "#" + saLevel, al)
              } else {
                db.getTranslation("SelfAssessFeedback_Match_Par1#" + itemLevel, al)
              }
            }

          val partTwo = {
              if (saLevel > itemLevel) {
                overEst
              } else if (saLevel == itemLevel) {
                accurate
              } else {
                underEst
              }
            }

          val map = Map("al" -> al,
                      "title" -> title,
                      "partOne" -> partOne,
                      "partTwo" -> partTwo,
                      "aboutSAText" -> aboutSAText)
          val output = engine.layout("src/main/resources/safeedback.mustache",map)
          val saFeedbackFile = new OutputStreamWriter(new FileOutputStream(new File(itemLevelDir,saLevel + ".html")),"UTF-8")
          saFeedbackFile.write(output)
          saFeedbackFile.close
        }
      }
    }
  }

  def exportTestResultPages(adminLanguages: List[String]): Unit = {

    val testresultsDir = new File(websiteDir,"testresults")
    if (!testresultsDir.isDirectory) {
        testresultsDir.mkdirs()
    }

    val levels = db.getItemLevels

    for (al <- adminLanguages) { 

      val backtooltip = db.getTranslation("Caption_BacktoWelcome",al)

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("backtooltip" -> backtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(testresultsDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()

      val alDir = new File(testresultsDir,al)
      if (!alDir.isDirectory) {
        alDir.mkdir()
      }

      val title = db.getTranslation("Title_DIALANGTestResults",al)

      for (skill <- db.testSkills) {

        val skillDir = new File(alDir,skill.toLowerCase)
        if (!skillDir.isDirectory) {
          skillDir.mkdir()
        }

        val explanTexts = levels.map(l => {
            val text = db.getTranslation("TestResults_Text#" + skill + "#" + l,al)
            ((l + "Explanation",text))
          })

        for (itemLevel <- levels) {
          val text = db.getTranslation("TestResults_Text#" + skill + "#" + itemLevel,al)
          val map = Map("al" -> al,
                      "title" -> title,
                      "text" -> text,
                      "itemLevel" -> itemLevel) ++ explanTexts
          val output = engine.layout("src/main/resources/testresults.mustache",map)
          val testresultsFile = new OutputStreamWriter(new FileOutputStream(new File(skillDir,itemLevel + ".html")),"UTF-8")
          testresultsFile.write(output)
          testresultsFile.close()
        }
      }
    }
  }

  def exportItemReviewPages(adminLanguages: List[String]): Unit = {

    val itemreviewDir = new File(websiteDir,"itemreview")
    if (!itemreviewDir.isDirectory) {
        itemreviewDir.mkdirs()
    }

    for (al <- adminLanguages) { 

      val title = db.getTranslation("Title_ItemReview",al)
      val text = db.getTranslation("ItemReview_Text",al)
      val backtooltip = db.getTranslation("Caption_BacktoFeedback",al)
      val subskills = 
        (db.getSubSkills(al).foldLeft(List.newBuilder[Map[String,String]])( (acc,curr) => {
              acc += Map("code" -> curr._1,"description" -> curr._2)
          })).result()
      val map = Map("title" -> title,"text" -> text,"subskills" -> subskills)
      val output = engine.layout("src/main/resources/itemreviewwrapper.mustache",map)
      val itemreviewFile = new OutputStreamWriter(new FileOutputStream(new File(itemreviewDir,al + ".html")),"UTF-8")
      itemreviewFile.write(output)
      itemreviewFile.close()

      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("backtooltip" -> backtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(itemreviewDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()
    }
  }

  def exportExplfbPages(adminLanguages: List[String]): Unit = {

    val aboutSADir = new File(websiteDir,"aboutsa")
    if (!aboutSADir.isDirectory) {
        aboutSADir.mkdirs()
    }

    for (al <- adminLanguages) {

      val backtooltip = db.getTranslation("Caption_BacktoFeedback",al)
      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("backtooltip" -> backtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(aboutSADir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()

      val alDir = new File(aboutSADir,al)
      if (!alDir.isDirectory) {
        alDir.mkdir()
      }

      val title = db.getTranslation("FeedbackOption_AboutSelfAssess",al)
      val mainHeader = db.getTranslation("Explanatory_Main_Header",al)
      val subHeader = db.getTranslation("Explanatory_Main_SubHeader",al)

      val howOften = db.getTranslation("Explanatory_Main_Menu_HowOften",al)
      val how = db.getTranslation("Explanatory_Main_Menu_Skills",al)
      val situationsDiffer = db.getTranslation("Explanatory_Main_Menu_Situations",al)
      val otherLearners = db.getTranslation("Explanatory_Main_Menu_OtherLearners",al)
      val otherTests = db.getTranslation("Explanatory_Main_Menu_OtherTests",al)
      val yourTargets = db.getTranslation("Explanatory_Main_Menu_Targets",al)
      val realLife = db.getTranslation("Explanatory_Main_Menu_RealLife",al)
      val otherReasons = db.getTranslation("Explanatory_Main_Menu_OtherReasons",al)

      val map = Map("title" -> title,
                      "mainHeader" -> mainHeader,
                      "subHeader" -> subHeader,
                      "howOften" -> howOften,
                      "how" -> how,
                      "situationsDiffer" -> situationsDiffer,
                      "otherLearners" -> otherLearners,
                      "otherTests" -> otherTests,
                      "yourTargets" -> yourTargets,
                      "realLife" -> realLife,
                      "otherReasons" -> otherReasons)
      val indexOutput = engine.layout("src/main/resources/aboutsashell.mustache",map)
      val aboutSAIndex = new OutputStreamWriter(new FileOutputStream(new File(alDir,"index.html")),"UTF-8")
      aboutSAIndex.write(indexOutput)
      aboutSAIndex.close()

      val main = db.getTranslation("Explanatory_Main_Text",al)
      val mainWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"main.html")),"UTF-8")
      mainWriter.write(main)
      mainWriter.close()

      doHowOften(al,alDir)
      doHow(al,alDir)
      doSituations(al,alDir)
      doOtherLearners(al,alDir)
      doOtherTests(al,alDir)
      doYourTargets(al,alDir)
      doRealLife(al,alDir)
      doOtherReasons(al,alDir)
    }
  }

  private def doHowOften(al: String, alDir: File): Unit = {

    val title = db.getTranslation("Explanatory_Main_Menu_HowOften",al)
    val howoften1 = db.getTranslation("ExpHowOften_Par1",al)
    val infrequently = db.getTranslation("ExpHowOften_Bullet1",al)
    val longtime = db.getTranslation("ExpHowOften_Bullet2",al)
    val howoften2 = db.getTranslation("ExpHowOften_Par2",al)
    val howOftenMap = Map("title" -> title,
                            "howoften1" -> howoften1,
                            "bullet1" -> infrequently,
                            "bullet2" -> longtime,
                            "howoften2" -> howoften2
                            )
    val howoftenOutput = engine.layout("src/main/resources/howoften.mustache",howOftenMap)
    val howOftenWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"howoften.html")),"UTF-8")
    howOftenWriter.write(howoftenOutput)
    howOftenWriter.close()

    val infrequentlyMap = Map("title" -> infrequently,
                            "part1" -> db.getTranslation("ExpInfrequently_Par1",al),
                            "part2" -> db.getTranslation("ExpInfrequently_Par2",al)
                            )
    val infrequentlyOutput = engine.layout("src/main/resources/twoparts.mustache",infrequentlyMap)
    val infrequentlyWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"infrequently.html")),"UTF-8")
    infrequentlyWriter.write(infrequentlyOutput)
    infrequentlyWriter.close()

    val longtime1 = db.getTranslation("ExpLongTime_Par1",al)
    val longtime2 = db.getTranslation("ExpLongTime_Par2",al)
    val longtimeMap = Map("title" -> longtime,
                            "part1" -> longtime1,
                            "part2" -> longtime2
                            )
    val longtimeOutput = engine.layout("src/main/resources/twoparts.mustache",longtimeMap)
    val longtimeWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"longtime.html")),"UTF-8")
    longtimeWriter.write(longtimeOutput)
    longtimeWriter.close()
  }

  private def doHow(al: String, alDir: File): Unit = {

    val howMap = Map("title" -> db.getTranslation("ExpSomeSkills_Head", al),
                            "part1" -> db.getTranslation("ExpSomeSkills_Par1", al),
                            "part2" -> db.getTranslation("ExpSomeSkills_Par2", al)
                            )
    val howOutput = engine.layout("src/main/resources/twoparts.mustache", howMap)
    val howWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir, "how.html")),"UTF-8")
    howWriter.write(howOutput)
    howWriter.close()

    val overestimateMap = Map("title" -> db.getTranslation("ExpOverestimate_Head",al),
                            "part1" -> db.getTranslation("ExpOverestimate_Par1",al),
                            "part2" -> db.getTranslation("ExpOverestimate_Par2",al)
                            )
    val overestimateOutput = engine.layout("src/main/resources/twoparts.mustache",overestimateMap)
    val overestimateWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"overestimate.html")),"UTF-8")
    overestimateWriter.write(overestimateOutput)
    overestimateWriter.close()

    val underestimateMap = Map("title" -> db.getTranslation("ExpUnderestimate_Head",al),
                            "part1" -> db.getTranslation("ExpUnderestimate_Par1",al)
                            )
    val underestimateOutput = engine.layout("src/main/resources/onepart.mustache",underestimateMap)
    val underestimateWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"underestimate.html")),"UTF-8")
    underestimateWriter.write(underestimateOutput)
    underestimateWriter.close()
  }

  private def doSituations(al: String, alDir: File): Unit = {

    val situtationsMap = Map("title" -> db.getTranslation("ExpSituation_Head",al),
                      "bullet1" -> db.getTranslation("ExpSituation_Bullet1",al),
                      "bullet2" -> db.getTranslation("ExpSituation_Bullet2",al),
                      "bullet3" -> db.getTranslation("ExpSituation_Bullet3",al)
                    )
    val situtationsOutput = engine.layout("src/main/resources/situations.mustache",situtationsMap)
    val situtationsWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"situations.html")),"UTF-8")
    situtationsWriter.write(situtationsOutput)
    situtationsWriter.close()
  }

  private def doOtherLearners(al: String, alDir: File): Unit = {

    val map = Map("title" -> db.getTranslation("ExpCompareOthers_Head",al),
                      "part1" -> db.getTranslation("ExpCompareOthers_Par1",al),
                      "part2" -> db.getTranslation("ExpCompareOthers_Par2",al)
                    )
    val output = engine.layout("src/main/resources/twoparts.mustache",map)
    val writer = new OutputStreamWriter(new FileOutputStream(new File(alDir,"otherlearners.html")),"UTF-8")
    writer.write(output)
    writer.close()
  }

  private def doOtherTests(al: String, alDir: File): Unit = {

    val map = Map("title" -> db.getTranslation("ExpOtherTests_Head",al),
                    "part1" -> db.getTranslation("ExpOtherTests_Par1",al),
                    "bullet1" -> db.getTranslation("ExpOtherTests_Bullet1",al),
                    "bullet2" -> db.getTranslation("ExpOtherTests_Bullet2",al),
                    "bullet3" -> db.getTranslation("ExpOtherTests_Bullet3",al),
                    "bullet4" -> db.getTranslation("ExpOtherTests_Bullet4",al),
                    "part2" -> db.getTranslation("ExpOtherTests_Par2",al)
                    )
    val output = engine.layout("src/main/resources/othertests.mustache",map)
    val writer = new OutputStreamWriter(new FileOutputStream(new File(alDir,"othertests.html")),"UTF-8")
    writer.write(output)
    writer.close()

    val dtMap = Map("title" -> db.getTranslation("ExpDiffTests_Head",al),
                    "part1" -> db.getTranslation("ExpDiffTests_Par1",al),
                    "part2" -> db.getTranslation("ExpDiffTests_Par2",al),
                    "part3" -> db.getTranslation("ExpDiffTests_Par3",al),
                    "part4" -> db.getTranslation("ExpDiffTests_Par4",al),
                    "part5" -> db.getTranslation("ExpDiffTests_Par5",al)
                    )
    val dtOutput = engine.layout("src/main/resources/differenttests.mustache",dtMap)
    val dtWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"differenttests.html")),"UTF-8")
    dtWriter.write(dtOutput)
    dtWriter.close()

    val sMap = Map("title" -> db.getTranslation("ExpSchoolTests_Head",al),
                    "part1" -> db.getTranslation("ExpSchoolTests_Par1",al),
                    "part2" -> db.getTranslation("ExpSchoolTests_Par2",al)
                    )
    val sOutput = engine.layout("src/main/resources/twoparts.mustache",sMap)
    val sWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"schooltests.html")),"UTF-8")
    sWriter.write(sOutput)
    sWriter.close()

    val wMap = Map("title" -> db.getTranslation("ExpWorkTests_Head",al),
                    "part1" -> db.getTranslation("ExpWorkTests_Par1",al)
                    )
    val wOutput = engine.layout("src/main/resources/onepart.mustache",wMap)
    val wWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"worktests.html")),"UTF-8")
    wWriter.write(wOutput)
    wWriter.close()

    val iMap = Map("title" -> db.getTranslation("ExpIntTests_Head",al),
                    "part1" -> db.getTranslation("ExpIntTests_Par1",al),
                    "part2" -> db.getTranslation("ExpIntTests_Par2",al)
                    )
    val iOutput = engine.layout("src/main/resources/twoparts.mustache",iMap)
    val iWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"internationaltests.html")),"UTF-8")
    iWriter.write(iOutput)
    iWriter.close()
  }

  private def doYourTargets(al: String, alDir: File): Unit = {

    val map = Map("title1" -> db.getTranslation("ExpTargets_Head1",al),
                    "part1" -> db.getTranslation("ExpTargets_Par1",al),
                    "part2" -> db.getTranslation("ExpTargets_Par2",al),
                    "title2" -> db.getTranslation("ExpTargets_Head2",al),
                    "part3" -> db.getTranslation("ExpTargets_Par3",al),
                    "part4" -> db.getTranslation("ExpTargets_Par4",al)
                    )
    val output = engine.layout("src/main/resources/yourtargets.mustache",map)
    val writer = new OutputStreamWriter(new FileOutputStream(new File(alDir,"yourtargets.html")),"UTF-8")
    writer.write(output)
    writer.close()
  }

  private def doRealLife(al: String, alDir: File): Unit = {

    val map = Map("title" -> db.getTranslation("ExpRealLife_Head",al),
                    "part1" -> db.getTranslation("ExpRealLife_Par1",al),
                    "part2" -> db.getTranslation("ExpRealLife_Par2",al),
                    "bullet1" -> db.getTranslation("ExpRealLife_Bullet1",al),
                    "bullet2" -> db.getTranslation("ExpRealLife_Bullet2",al),
                    "bullet3" -> db.getTranslation("ExpRealLife_Bullet3",al),
                    "bullet4" -> db.getTranslation("ExpRealLife_Bullet4",al),
                    "bullet5" -> db.getTranslation("ExpRealLife_Bullet5",al),
                    "bullet6" -> db.getTranslation("ExpRealLife_Bullet6",al)
                    )
    val output = engine.layout("src/main/resources/reallife.mustache",map)
    val writer = new OutputStreamWriter(new FileOutputStream(new File(alDir,"reallife.html")),"UTF-8")
    writer.write(output)
    writer.close()

    val aMap = Map("title" -> db.getTranslation("ExpAnxiety_Head",al),
                    "part1" -> db.getTranslation("ExpAnxiety_Par1",al),
                    "part2" -> db.getTranslation("ExpAnxiety_Par2",al)
                    )
    val aOutput = engine.layout("src/main/resources/twoparts.mustache",aMap)
    val aWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"anxiety.html")),"UTF-8")
    aWriter.write(aOutput)
    aWriter.close()

    val tMap = Map("title" -> db.getTranslation("ExpTimeAllowed_Head",al),
                    "part1" -> db.getTranslation("ExpTimeAllowed_Par1",al),
                    "part2" -> db.getTranslation("ExpTimeAllowed_Par2",al),
                    "part3" -> db.getTranslation("ExpTimeAllowed_Par3",al)
                    )
    val tOutput = engine.layout("src/main/resources/threeparts.mustache",tMap)
    val tWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"timeallowed.html")),"UTF-8")
    tWriter.write(tOutput)
    tWriter.close()

    val sMap = Map("title" -> db.getTranslation("ExpSupport_Head",al),
                    "part1" -> db.getTranslation("ExpSupport_Par1",al)
                    )
    val sOutput = engine.layout("src/main/resources/onepart.mustache",sMap)
    val sWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"support.html")),"UTF-8")
    sWriter.write(sOutput)
    sWriter.close()

    val nMap = Map("title" -> db.getTranslation("ExpNumber_Head",al),
                    "part1" -> db.getTranslation("ExpNumber_Par1",al)
                    )
    val nOutput = engine.layout("src/main/resources/onepart.mustache",nMap)
    val nWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"number.html")),"UTF-8")
    nWriter.write(nOutput)
    nWriter.close()

    val fMap = Map("title" -> db.getTranslation("ExpFamiliarity_Head",al),
                    "part1" -> db.getTranslation("ExpFamiliarity_Par1",al)
                    )
    val fOutput = engine.layout("src/main/resources/onepart.mustache",fMap)
    val fWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"familiarity.html")),"UTF-8")
    fWriter.write(fOutput)
    fWriter.close()

    val mMap = Map("title" -> db.getTranslation("ExpMedium_Head",al),
                    "part1" -> db.getTranslation("ExpMedium_Par1",al)
                    )
    val mOutput = engine.layout("src/main/resources/onepart.mustache",mMap)
    val mWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"medium.html")),"UTF-8")
    mWriter.write(mOutput)
    mWriter.close()
  }

  private def doOtherReasons(al: String, alDir: File): Unit = {

    val map = Map("title1" -> db.getTranslation("ExpOtherReasons_Head1",al),
                    "part1" -> db.getTranslation("ExpOtherReasons_Par1",al),
                    "bullet1" -> db.getTranslation("ExpOtherReasons_Bullet1",al),
                    "bullet2" -> db.getTranslation("ExpOtherReasons_Bullet2",al),
                    "part2" -> db.getTranslation("ExpOtherReasons_Par2",al),
                    "title2" -> db.getTranslation("ExpOtherReasons_Head2",al),
                    "part3" -> db.getTranslation("ExpTargets_Par3",al),
                    "part4" -> db.getTranslation("ExpTargets_Par4",al)
                    )
    val output = engine.layout("src/main/resources/otherreasons.mustache",map)
    val writer = new OutputStreamWriter(new FileOutputStream(new File(alDir,"otherreasons.html")),"UTF-8")
    writer.write(output)
    writer.close()
  }

  def exportAdvfbPages(adminLanguages: List[String]): Unit = {

    val advfbDir = new File(websiteDir,"advfb")
    if (!advfbDir.isDirectory) {
        advfbDir.mkdirs()
    }

    val tls = db.getTestLanguageCodes

    for (al <- adminLanguages) {

      val backtooltip = db.getTranslation("Caption_BacktoFeedback",al)
      val tipOutput = engine.layout("src/main/resources/toolbartooltips.mustache",Map("backtooltip" -> backtooltip))
      val tipFile = new OutputStreamWriter(new FileOutputStream(new File(advfbDir,al + "-toolbarTooltips.json")),"UTF-8")
      tipFile.write(tipOutput)
      tipFile.close()

      val alDir = new File(advfbDir,al)
      if (!alDir.isDirectory) {
        alDir.mkdir()
      }

      val chooselevel = db.getTranslation("Caption_ChooseLevel",al)
      val howtoimprove = db.getTranslation("Caption_HowtoImprove",al)
      val shellOutput = engine.layout("src/main/resources/advfbshell.mustache",Map("chooselevel" -> chooselevel,"howtoimprove" -> howtoimprove))
      val shellWriter = new OutputStreamWriter(new FileOutputStream(new File(alDir,"index.html")),"UTF-8")
      shellWriter.write(shellOutput)
      shellWriter.close()

      val a1Header = db.getTranslation("AdvisoryTable_Intro_#A1",al)
      val a2Header = db.getTranslation("AdvisoryTable_Intro_#A2",al)
      val b1Header = db.getTranslation("AdvisoryTable_Intro_#B1",al)
      val b2Header = db.getTranslation("AdvisoryTable_Intro_#B2",al)
      val c1Header = db.getTranslation("AdvisoryTable_Intro_#C1",al)
      val c2Header = db.getTranslation("AdvisoryTable_Intro_#C2",al)

      for (skill <- db.advfbSkills) {

        val skillDir = new File(alDir,skill.toLowerCase)
        if (!skillDir.isDirectory) {
          skillDir.mkdir()
        }

        val a1Map = Map(
            "header" -> a1Header,
            "row1heading" -> db.getTranslation("AdvisoryTable_Row1_Heading_#" + skill,al),
            "row1texta1" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#A1",al),
            "row1texta2" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#A2",al),
            "row2heading" -> db.getTranslation("AdvisoryTable_Row2_Heading_#" + skill,al),
            "row2texta1" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#A1",al),
            "row2texta2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#A2",al),
            "row3heading" -> db.getTranslation("AdvisoryTable_Row3_Heading",al),
            "row3texta1" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#A1",al),
            "row3texta2" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#A2",al))
        val a1Output = engine.layout("src/main/resources/advfba1.mustache",a1Map)
        val a1Writer = new OutputStreamWriter(new FileOutputStream(new File(skillDir,"A1.html")),"UTF-8")
        a1Writer.write(a1Output)
        a1Writer.close()

        val a2Map = Map(
            "header" -> a2Header,
            "row1heading" -> db.getTranslation("AdvisoryTable_Row1_Heading_#" + skill,al),
            "row1texta1" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#A1",al),
            "row1texta2" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#A2",al),
            "row1textb1" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#B1",al),
            "row2heading" -> db.getTranslation("AdvisoryTable_Row2_Heading_#" + skill,al),
            "row2texta1" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#A1",al),
            "row2texta2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#A2",al),
            "row2textb1" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#B1",al),
            "row3heading" -> db.getTranslation("AdvisoryTable_Row3_Heading",al),
            "row3texta1" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#A1",al),
            "row3texta2" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#A2",al),
            "row3textb1" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#B1",al))
        val a2Output = engine.layout("src/main/resources/advfba2.mustache",a2Map)
        val a2Writer = new OutputStreamWriter(new FileOutputStream(new File(skillDir,"A2.html")),"UTF-8")
        a2Writer.write(a2Output)
        a2Writer.close()

        val b1Map = Map(
            "header" -> b1Header,
            "row1heading" -> db.getTranslation("AdvisoryTable_Row1_Heading_#" + skill,al),
            "row1texta2" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#A2",al),
            "row1textb1" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#B1",al),
            "row1textb2" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#B2",al),
            "row2heading" -> db.getTranslation("AdvisoryTable_Row2_Heading_#" + skill,al),
            "row2texta2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#A2",al),
            "row2textb1" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#B1",al),
            "row2textb2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#B2",al),
            "row3heading" -> db.getTranslation("AdvisoryTable_Row3_Heading",al),
            "row3texta2" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#A2",al),
            "row3textb1" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#B1",al),
            "row3textb2" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#B2",al))
        val b1Output = engine.layout("src/main/resources/advfbb1.mustache",b1Map)
        val b1Writer = new OutputStreamWriter(new FileOutputStream(new File(skillDir,"B1.html")),"UTF-8")
        b1Writer.write(b1Output)
        b1Writer.close()

        val b2Map = Map(
            "header" -> b2Header,
            "row1heading" -> db.getTranslation("AdvisoryTable_Row1_Heading_#" + skill,al),
            "row1textb1" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#B1",al),
            "row1textb2" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#B2",al),
            "row1textc1" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#C1",al),
            "row2heading" -> db.getTranslation("AdvisoryTable_Row2_Heading_#" + skill,al),
            "row2textb1" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#B1",al),
            "row2textb2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#B2",al),
            "row2textc2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#C1",al),
            "row3heading" -> db.getTranslation("AdvisoryTable_Row3_Heading",al),
            "row3textb1" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#B1",al),
            "row3textb2" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#B2",al),
            "row3textc1" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#C1",al))
        val b2Output = engine.layout("src/main/resources/advfbb2.mustache",b2Map)
        val b2Writer = new OutputStreamWriter(new FileOutputStream(new File(skillDir,"B2.html")),"UTF-8")
        b2Writer.write(b2Output)
        b2Writer.close()

        val c1Map = Map(
            "header" -> c1Header,
            "row1heading" -> db.getTranslation("AdvisoryTable_Row1_Heading_#" + skill,al),
            "row1textb2" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#B2",al),
            "row1textc1" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#C1",al),
            "row1textc2" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#C2",al),
            "row2heading" -> db.getTranslation("AdvisoryTable_Row2_Heading_#" + skill,al),
            "row2textb2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#B2",al),
            "row2textc1" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#C1",al),
            "row2textc2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#C2",al),
            "row3heading" -> db.getTranslation("AdvisoryTable_Row3_Heading",al),
            "row3textb2" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#B2",al),
            "row3textc1" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#C1",al),
            "row3textc2" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#C2",al))
        val c1Output = engine.layout("src/main/resources/advfbc1.mustache",c1Map)
        val c1Writer = new OutputStreamWriter(new FileOutputStream(new File(skillDir,"C1.html")),"UTF-8")
        c1Writer.write(c1Output)
        c1Writer.close()

        val c2Map = Map(
            "header" -> c2Header,
            "row1heading" -> db.getTranslation("AdvisoryTable_Row1_Heading_#" + skill,al),
            "row1textc1" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#C1",al),
            "row1textc2" -> db.getTranslation("AdvisoryTable_Row1_Text_#" + skill + "_#C2",al),
            "row2heading" -> db.getTranslation("AdvisoryTable_Row2_Heading_#" + skill,al),
            "row2textc1" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#C1",al),
            "row2textc2" -> db.getTranslation("AdvisoryTable_Row2_Text_#" + skill + "_#C2",al),
            "row3heading" -> db.getTranslation("AdvisoryTable_Row3_Heading",al),
            "row3textc1" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#C1",al),
            "row3textc2" -> db.getTranslation("AdvisoryTable_Row3_Text_#" + skill + "_#C2",al))
        val c2Output = engine.layout("src/main/resources/advfbc2.mustache",c2Map)
        val c2Writer = new OutputStreamWriter(new FileOutputStream(new File(skillDir,"C2.html")),"UTF-8")
        c2Writer.write(c2Output)
        c2Writer.close()

        for (t <- tls) {
          val tl = t._1
          val twoLetterCode = t._2

          val tlDir = new File(skillDir,t._1)
          if (!tlDir.isDirectory) {
            tlDir.mkdir()
          }

          if (skill == "Reading") {
            val a1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#A1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A1_#Item1_#" + twoLetterCode,al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A1_#Item2_#" + twoLetterCode,al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A1_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A1_#Item4",al),
              "item5" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A1_#Item5_#" + twoLetterCode,al),
              "item6" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A1_#Item6_#" + twoLetterCode,al))
            val a1Output = engine.layout("src/main/resources/advfb6itemadvice.mustache",a1Map)
            val a1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"A1.html")),"UTF-8")
            a1Writer.write(a1Output)
            a1Writer.close()

            val a2Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#A2",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A2_#Item1_#" + twoLetterCode,al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A2_#Item2_#" + twoLetterCode,al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A2_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#A2_#Item4_#" + twoLetterCode,al))
            val a2Output = engine.layout("src/main/resources/advfb4itemadvice.mustache",a2Map)
            val a2Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"A2.html")),"UTF-8")
            a2Writer.write(a2Output)
            a2Writer.close()

            val b1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#B1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#B1_#Item1_#" + twoLetterCode,al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#B1_#Item2",al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#B1_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#B1_#Item4",al))
            val b1Output = engine.layout("src/main/resources/advfb4itemadvice.mustache",b1Map)
            val b1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"B1.html")),"UTF-8")
            b1Writer.write(b1Output)
            b1Writer.close()

            val b2Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#B2",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#B2_#Item1",al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#B2_#Item2_#" + twoLetterCode,al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#B2_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#B2_#Item4",al))
            val b2Output = engine.layout("src/main/resources/advfb4itemadvice.mustache",b2Map)
            val b2Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"B2.html")),"UTF-8")
            b2Writer.write(b2Output)
            b2Writer.close()

            val c1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#C1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#C1_#Item1",al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#C1_#Item2",al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#C1_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#C1_#Item4_#" + twoLetterCode,al),
              "item5" -> db.getTranslation("AdvisoryTips_Bullet_#Reading_#C1_#Item5_#" + twoLetterCode,al))
            val c1Output = engine.layout("src/main/resources/advfb5itemadvice.mustache",c1Map)
            val c1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"C1.html")),"UTF-8")
            c1Writer.write(c1Output)
            c1Writer.close()
          } // Reading
          else if (skill == "Writing") {
            val a1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#A1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A1_#Item1_#" + twoLetterCode,al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A1_#Item2_#" + twoLetterCode,al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A1_#Item3_#" + twoLetterCode,al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A1_#Item4",al),
              "item5" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A1_#Item5_#" + twoLetterCode,al))
            val a1Output = engine.layout("src/main/resources/advfb5itemadvice.mustache",a1Map)
            val a1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"A1.html")),"UTF-8")
            a1Writer.write(a1Output)
            a1Writer.close()

            val a2Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#A2",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A2_#Item1",al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A2_#Item2_#" + twoLetterCode,al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A2_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A2_#Item4_#" + twoLetterCode,al),
              "item5" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#A2_#Item5_#" + twoLetterCode,al))
            val a2Output = engine.layout("src/main/resources/advfb5itemadvice.mustache",a2Map)
            val a2Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"A2.html")),"UTF-8")
            a2Writer.write(a2Output)
            a2Writer.close()

            val b1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#B1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#B1_#Item1",al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#B1_#Item2",al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#B1_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#B1_#Item4",al))
            val b1Output = engine.layout("src/main/resources/advfb4itemadvice.mustache",b1Map)
            val b1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"B1.html")),"UTF-8")
            b1Writer.write(b1Output)
            b1Writer.close()

            val b2Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#B2",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#B2_#Item1",al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#B2_#Item2",al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#B2_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#B2_#Item4",al))
            val b2Output = engine.layout("src/main/resources/advfb4itemadvice.mustache",b2Map)
            val b2Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"B2.html")),"UTF-8")
            b2Writer.write(b2Output)
            b2Writer.close()

            val c1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#C1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#C1_#Item1",al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#C1_#Item2",al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#C1_#Item3",al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#C1_#Item4",al),
              "item5" -> db.getTranslation("AdvisoryTips_Bullet_#Writing_#C1_#Item5",al))
            val c1Output = engine.layout("src/main/resources/advfb5itemadvice.mustache",c1Map)
            val c1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"C1.html")),"UTF-8")
            c1Writer.write(c1Output)
            c1Writer.close()
          } // Writing
          else if (skill == "Listening") {
            val dontUnderstand = "'" + db.getTranslation("Utterances_DontUnderstand",tl) + "'"
            val pleaseRepeat = "'" + db.getTranslation("Utterances_PleaseRepeat",tl) + "'"
            val sayAgain = "'" + db.getTranslation("Utterances_SayAgain",tl) + "'"
            val speakSlowly = "'" + db.getTranslation("Utterances_SpeakSlowly",tl) + "'"
            val item4 = db.getTranslation("AdvisoryTips_Bullet_#Listening_#A1_#Item4", al)
                .replaceFirst("<utterance>Utterances_DontUnderstand</utterance>", dontUnderstand)
                .replaceFirst("<utterance>Utterances_PleaseRepeat</utterance>",pleaseRepeat)
                .replaceFirst("<utterance>Utterances_SayAgain</utterance>",sayAgain)
                .replaceFirst("<utterance>Utterances_SpeakSlowly</utterance>",speakSlowly)
            val a1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#A1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#A1_#Item1",al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#A1_#Item2_#" + twoLetterCode,al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#A1_#Item3",al),
              "item4" -> item4)
            val a1Output = engine.layout("src/main/resources/advfb4itemadvice.mustache",a1Map)
            val a1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"A1.html")),"UTF-8")
            a1Writer.write(a1Output)
            a1Writer.close()

            val a2Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#A2",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#A2_#Item1",al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#A2_#Item2",al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#A2_#Item3_#" + twoLetterCode,al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#A2_#Item4",al))
            val a2Output = engine.layout("src/main/resources/advfb4itemadvice.mustache",a2Map)
            val a2Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"A2.html")),"UTF-8")
            a2Writer.write(a2Output)
            a2Writer.close()

            val b1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#B1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#B1_#Item1_#" + twoLetterCode,al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#B1_#Item2_#" + twoLetterCode,al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#B1_#Item3_#" + twoLetterCode,al),
              "item4" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#B1_#Item4",al))
            val b1Output = engine.layout("src/main/resources/advfb4itemadvice.mustache",b1Map)
            val b1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"B1.html")),"UTF-8")
            b1Writer.write(b1Output)
            b1Writer.close()

            val b2Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#B2",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#B2_#Item1_#" + twoLetterCode,al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#B2_#Item2",al),
              "item3" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#B2_#Item3",al))
            val b2Output = engine.layout("src/main/resources/advfb3itemadvice.mustache",b2Map)
            val b2Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"B2.html")),"UTF-8")
            b2Writer.write(b2Output)
            b2Writer.close()

            val c1Map = Map(
              "header" -> db.getTranslation("AdvisoryTips_Intro_#C1",al),
              "item1" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#C1_#Item1_#" + twoLetterCode,al),
              "item2" -> db.getTranslation("AdvisoryTips_Bullet_#Listening_#C1_#Item2_#" + twoLetterCode,al))
            val c1Output = engine.layout("src/main/resources/advfb2itemadvice.mustache",c1Map)
            val c1Writer = new OutputStreamWriter(new FileOutputStream(new File(tlDir,"C1.html")),"UTF-8")
            c1Writer.write(c1Output)
            c1Writer.close()
          } // Listening

        } // tl
      }
    }
  }
}
"""
