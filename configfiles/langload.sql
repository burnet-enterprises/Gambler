-- import to SQLite by running: sqlite3.exe db.sqlite3 -init sqlite.sql

PRAGMA journal_mode = MEMORY;
PRAGMA synchronous = OFF;
PRAGMA foreign_keys = OFF;
PRAGMA ignore_check_constraints = OFF;
PRAGMA auto_vacuum = NONE;
PRAGMA secure_delete = OFF;
BEGIN TRANSACTION;

Insert INTO `LangUserGenderRaceSystemTranslate`
(language_id,demographics_language,demographics_country,demographics_gender,demographics_gender_default,demographics_race,demographics_race_default)
VALUES
(2, "es-ES","USA","{'F':'Mujer','M':'Hombre','O':'Otro'}", "O", "{'blk': 'Africana/Afroamericana', 'asn': 'Asiática', 'hpi': 'Hawaiana/ Islas del Pacífico', 'nam': 'Indígena/ Alaska americana', 'mna': 'Oriente medio/ Norteafricana', 'wht': 'Blanca'}","blk")
INSERT INTO `LangCode` VALUES (1,'en-US','United States English');
INSERT INTO `LangUserGenderRaceSystemTranslate` VALUES (3,'en-CA','USA','{''F'':''Female'',''M'':''Male'',''O'':''Non-binary/Other''}','O','{''blk'': ''African/Black American'', ''asn'': ''Asian'', ''hpi'': ''Hawaiian/Pacific Islander'', ''nam'': ''Native/Alsaka American'', ''mna'': ''Middle Eastern/North African'', ''wht'': ''White''} ','blk');
INSERT INTO `LangUserSystemTranslate` VALUES (3,'Hello','Continue','Show less information','Show more information','The Gambler','','''Welcome, press start to begin.''','Start','Icon','Health State','Health State Abbreviations','''Here are the following health states, their icons, their abbreviations, and their information.''','Information','Double click on a health state icon to see a video clip description of the health state.','Each of the images that represents health states are drag and droppable.Please drag each image into the empty box ordering them from best to worst state (top to bottom)','Video Instructions','''Sorry, you may have forgotten to order the states.<br/>Please drag each image into the empty box ordering them from best to worst state (top to bottom).''','Click and drag the icon on the sliders to show your values for each health state.','''Sorry, you may have forgotten to click and drag the sliders.<br/>Click and drag the icon on the sliders to show your values for each health state.''','Video Instructions','Performing General Standard Gamble Video Instructions','Performing Standard Gamble for {{MainCondition}} Video Instructions','Performing General Time Trade off Video Instructions','Performing Time Trade off for {{MainCondition}} Video Instructions','Health State','Ordinal Scale','Visual Analog Scale','Standard Gamble','Time Trade off','CSV Export','Finish','en-CA','Thank you for completing the assessement {{FirstName}}.Here are the results: ','User ID','First name','Last name','Age','Hispanic/Latino','Gender','Race','Click here to turn off video instructions','Please enter your first name.','Please enter your last name.','Please enter your age.','Please enter your information.','Shake','Pill(s)','Month(s)','Years')





COMMIT;
PRAGMA ignore_check_constraints = ON;
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
