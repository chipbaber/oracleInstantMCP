# How to Create a MCP Server with Tools to Access a 26ai Autonomous Database Tables & Procedures
 Do you have an existing Oracle database with years of tables, procedures, and functional code? Do you want to expose a piece of this database to LLMs to more rapidly assist users in performing required actions? Are you curious to see how easy it is to develop with MCP against an Autonomous AI database in the Cloud? Then this 12-minute getting-started video is for you.

The example code and video below will walk you through an introductory look at how to create your first MCP server to access an Oracle Autonomous AI database, leveraging Python and FastMCP libraries. The video begins by creating a new database user inside a 26ai ATP-S database in the Cloud. Once created, we will showcase how to create a connection to the user account via VS Code and quickly install a sample table, load data, and install a sample PL/SQL procedure to be leveraged by our MCP server. Next, we will show how to create a bash profile with the required connection information to access our 26ai database and install the required Python libraries locally to run FastMCP. With the setup complete, we will walk through step-by-step each line of code on how to create your first MCP tool. The tool will input a parameter, use the parameter in a query that returns values from a table as a JSON payload. With our first MCP Server tool ready, we will showcase how to access the tool from a command-line client to test our connection to the 26ai database and check for the desired data results. With the baseline knowledge in hand, we will add a second MCP tool that demonstrates how to call a database procedure with multiple input and output variables. We will walk the viewer through how to properly annotate the input and output variables to help your LLM better understand the MCP tool's desired action and how to interact with it. Finally, we will add a third tool that inputs a table name and returns the table's column comments to help the LLM understand the context of the data returned from our query or to understand how to better query a table. With all the code ready, we will add our MCP server directly to our VS Code development environment and call it directly from the embedded co-pilot chat session to demonstrate how the LLM can leverage the tools individually or in multiple steps to perform a desired action on only a subset of 26ai database objects. Please note that this code and demo should be compatible with 19c and/or 23ai ADB-S databases and, with slight modifications to connect strings, most any Oracle database.


# Watch the Online Demo
Before proceding with the instructions below please watch the demo video to provide context and to use as a reference when performing the technical actions below. [https://youtu.be/54CrrW7t3iQ](https://youtu.be/54CrrW7t3iQ)
Please note the MCP tool code in the video is saved in 26ai_fastmcp. 

# Pre-requisites to Replicate Steps Show in Video
The steps below were down before the video record on the development machine. For this examples the recorded leveraged Windows 10. This can be easily repeated on other operating systems.
- If using windows you will need to install Git Bash to replicate what is shown inside the video. [https://gitforwindows.org/](https://gitforwindows.org/)
- You will need to have python installed and pip enabled on install for your development machine. [https://www.python.org/downloads/](https://www.python.org/downloads/)
- You will need an Oracle Cloud Infrastructure environment. Link to free tier:  [https://www.oracle.com/cloud/free/](https://www.oracle.com/cloud/free/)
- Install a 26ai database on OCI and learn how to access the Database Actions SQL Studio watch: [https://youtu.be/a350ebLzyV0](https://youtu.be/a350ebLzyV0)
- To download and install the Oracle Instant Client, SQL*Plus and your a 26ai Database Wallet. Please watch this instructional video: [https://youtu.be/DyJRgrMDPx8](https://youtu.be/DyJRgrMDPx8)
- Follow the steps in this video install Visual Studio Code, connect to co-pilot and Oracle VS Studio plugin. [https://www.youtube.com/watch?v=TvQb7H11zYM&list=PLsnBif_-5JnA8Hzvp8e1bQ3fo6VEvYEB0&index=4&pp=gAQBiAQB](https://www.youtube.com/watch?v=TvQb7H11zYM&list=PLsnBif_-5JnA8Hzvp8e1bQ3fo6VEvYEB0&index=4&pp=gAQBiAQB)


# Create a User in the Database
- Open Database Actions SQL Studio from your OCI console. As admin, create the players user for the sample demo. 
![](assets/2025-10-28-11-22-02.png)

```
create user players identified by "{password}";
grant dwrole to players;
grant unlimited tablespace to players;
```

# Create Database Objects 
- Open Visual Studio Code and the Oracle VS Studio Plugin and create a connection to your 26ai database. Connect as the players user created in the prior step.  
![](assets/2025-10-28-11-30-04.png)


- Right click on your new connection and open SQL Worksheet. 
![](assets/2025-10-30-14-52-52.png)

-  Paste in the statements below to create the required objects for the mcp server will access in our demo.
```
 CREATE TABLE "TEAMSTATS" 
   (	"ID" NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 13 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  NOT NULL ENABLE, 
	"JERSEY" NUMBER, 
	"NAME" VARCHAR2(100), 
	"GP" NUMBER, 
	"PA" NUMBER, 
	"AB" NUMBER, 
	"H" NUMBER, 
	"C1B" NUMBER, 
	"C2B" NUMBER, 
	"C3B" NUMBER, 
	"HR" NUMBER, 
	"RBI" NUMBER, 
	"R" NUMBER, 
	"BB" NUMBER, 
	"SO" NUMBER, 
	"K_L" NUMBER, 
	"HBP" NUMBER, 
	"SAC" NUMBER, 
	"SF" NUMBER, 
	"ROE" NUMBER, 
	"FC" NUMBER, 
	"SB" NUMBER, 
	"QAB" NUMBER, 
	"QAB_" NUMBER, 
	"LOB" NUMBER, 
	"XBH" NUMBER, 
	"TB" NUMBER, 
	"PS" NUMBER, 
	"AVG" NUMBER GENERATED ALWAYS AS (ROUND("H"/"AB",3)) VIRTUAL , 
	"OBP" NUMBER GENERATED ALWAYS AS (ROUND(("H"+"BB"+"HBP")/("AB"+"BB"+"HBP"+"SAC"),3)) VIRTUAL , 
	"SLG" NUMBER GENERATED ALWAYS AS (ROUND("TB"/"AB",3)) VIRTUAL , 
	"VIDEO" VARCHAR2(2500), 
	 PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   ) ;
```

- Add the following table and column comments. 
```
COMMENT ON COLUMN "TEAMSTATS"."JERSEY" IS 'The jersey number of the player';
   COMMENT ON COLUMN "TEAMSTATS"."NAME" IS 'The name number of the baseball player';
   COMMENT ON COLUMN "TEAMSTATS"."GP" IS 'The number of games played by the baseball player';
   COMMENT ON COLUMN "TEAMSTATS"."PA" IS 'The number of plate appearances by the baseball player';
   COMMENT ON COLUMN "TEAMSTATS"."AB" IS 'The number of at bats by the baseball player. An official at-bat comes when a batter reaches base via a fielders choice, hit or an error (not including catchers interference) or when a batter is put out on a non-sacrifice.';
   COMMENT ON COLUMN "TEAMSTATS"."H" IS 'The number of hits by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."C1B" IS 'The number of singles by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."C2B" IS 'The number of doubles by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."C3B" IS 'The number of triples by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."HR" IS 'The number of homeruns by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."RBI" IS 'The number of runs batted in by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."R" IS 'total runs scored';
   COMMENT ON COLUMN "TEAMSTATS"."BB" IS 'The number of base on balls by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."SO" IS 'The number of strikeouts by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."K_L" IS 'Strikeouts looking (K_L) represents the number of times a batter strikes out without swinging at the final strike. It is a direct count and not derived from other columns.';
   COMMENT ON COLUMN "TEAMSTATS"."HBP" IS 'The number of hit by pitches by a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."SAC" IS 'Sacrifice (SAC) represents the number of times a batter advances a runner by sacrificing their at-bat, typically through a bunt or fly ball. It is a direct count and not derived from other columns.';
   COMMENT ON COLUMN "TEAMSTATS"."SF" IS 'Sacrifice flies (SF) represents the number of times a batter hits a fly ball that allows a runner to score while the batter is out. It is a direct count and not derived from other columns.';
   COMMENT ON COLUMN "TEAMSTATS"."ROE" IS 'Reached on error (ROE) represents the number of times a batter reaches base due to a fielding error by the opposing team. It is a direct count and not derived from other columns.';
   COMMENT ON COLUMN "TEAMSTATS"."FC" IS 'Fielder''s choice (FC) represents the number of times a batter reaches base due to a fielder choosing to make a play on another runner. It is a direct count and not derived from other columns.';
   COMMENT ON COLUMN "TEAMSTATS"."SB" IS 'total stolen bases by the player during the season.';
   COMMENT ON COLUMN "TEAMSTATS"."QAB" IS 'The number of quality at bats for a player in a season';
   COMMENT ON COLUMN "TEAMSTATS"."QAB_" IS 'The percentage calculation of quality at bats for a player in a season. for example 46.55 is 46.55% of quality at bats. ';
   COMMENT ON COLUMN "TEAMSTATS"."LOB" IS 'total runners left on base when the player was at bat during the season.';
   COMMENT ON COLUMN "TEAMSTATS"."XBH" IS 'total extra base hits by a player during the season.';
   COMMENT ON COLUMN "TEAMSTATS"."TB" IS 'Total bases (TB) represents the total number of bases a batter has gained from hits. It is calculated as the sum of singles (H - XBH - HR), doubles (2 * (C2B)), triples (3 * (C3B)), and home runs (4 * HR). Formula: TB = (H - XBH - HR) + (2 * C2B) + (3 * C3B) + (4 * HR).';
   COMMENT ON COLUMN "TEAMSTATS"."PS" IS 'Plate appearances per strikeout (PS) represents the average number of plate appearances a batter has before striking out. It is calculated as plate appearances (PA) divided by strikeouts (SO). Formula: PS = PA / SO.';
   COMMENT ON COLUMN "TEAMSTATS"."AVG" IS 'The batting average of the player rounded to 3 decimal places as calculated by the number of hits divided by the number of at bats in a season';
   COMMENT ON COLUMN "TEAMSTATS"."OBP" IS 'The on base percentage for player rounded to 3 decimal places as calculated by (H+BB+HBP)/(AB+BB+HBP+SAC) in a season';
   COMMENT ON COLUMN "TEAMSTATS"."SLG" IS 'Slugging percentage (SLG) is a measure of the batting productivity of a hitter. It is calculated as total bases (TB) divided by at-bats (AB). Formula: SLG = TB / AB.';
   COMMENT ON TABLE "TEAMSTATS"  IS 'This table the player statistics for the 2023 baseball season.';
```

- Insert some sample data in the table.
```
begin
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (1, 'Nathaniel', 20, 49, 21, 19, 9, 6, 2, 2, 10, 35, 11, 5, 2, 11, 3, 11, 1, 1, 5, 1, 15, 58, 27, 46.55, 198, '4', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (2, 'Jack', 14, 24, 9, 5, 4, 1, 0, 0, 1, 6, 1, 10, 0, 6, 3, 3, 0, 0, 0, 0, 23, 34, 21, 61.76, 159, '7', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (3, 'Brodie', 20, 53, 30, 26, 15, 4, 3, 4, 11, 48, 22, 5, 3, 4, 0, 22, 1, 0, 5, 1, 16, 62, 35, 56.45, 225, '8', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (4, 'Kellan', 20, 49, 20, 19, 9, 9, 0, 1, 10, 31, 11, 11, 1, 5, 1, 9, 0, 0, 4, 0, 24, 61, 28, 45.9, 231, '9', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (5, 'Tank', 18, 47, 15, 18, 8, 7, 1, 2, 10, 33, 27, 4, 3, 4, 1, 8, 0, 0, 2, 2, 19, 54, 25, 46.3, 178, '11', 'https://youtu.be/kz1E99o0KEU');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (6, 'Ben', 14, 25, 7, 8, 7, 1, 0, 0, 1, 9, 6, 3, 0, 4, 1, 0, 0, 0, 2, 1, 14, 28, 10, 35.71, 113, '17', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (7, 'Noah', 20, 35, 7, 8, 7, 1, 0, 0, 1, 9, 3, 9, 0, 9, 2, 1, 1, 0, 1, 1, 22, 45, 23, 51.11, 180, '21', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (8, 'Kaleb', 20, 46, 10, 14, 9, 3, 0, 2, 5, 23, 12, 9, 1, 8, 3, 6, 1, 1, 0, 0, 23, 58, 25, 43.1, 187, '22', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (9, 'Chase', 20, 38, 11, 11, 8, 3, 0, 0, 3, 14, 8, 10, 1, 10, 5, 1, 0, 0, 0, 2, 29, 50, 22, 44, 205, '23', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (10, 'Canir', 19, 32, 7, 6, 5, 1, 0, 0, 1, 7, 5, 10, 0, 10, 4, 3, 0, 0, 0, 1, 31, 42, 19, 45.24, 189, '27', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (11, 'Matthew', 18, 36, 9, 12, 9, 3, 0, 0, 3, 15, 8, 8, 0, 6, 1, 1, 0, 0, 3, 2, 17, 44, 20, 45.45, 155, '28', '');
    insert into teamstats (id, name, gp, ab, r, h, c1b, c2b, c3b, hr, xbh, tb, rbi, bb, hbp, so, k_l, sb, sf, sac, roe, fc, lob, pa, qab, qab_, ps, jersey, video) 
    values (12, 'Charles', 20, 37, 9, 9, 8, 1, 0, 0, 1, 10, 5, 13, 2, 4, 1, 3, 0, 0, 3, 2, 18, 52, 24, 46.15, 194, '99', '');
    commit;
end;
/
```

- Create the myStats procedure to simulate a calculation for our example.
```
CREATE OR REPLACE PROCEDURE myStats(
    p_atBats IN NUMBER,
    p_hits IN NUMBER,
    p_walks_hbp IN NUMBER,
    p_sac IN NUMBER,
    p_battingAvg OUT NUMBER,
    p_onBasePercentage OUT NUMBER
) IS
BEGIN
    -- Check for division by zero
    IF p_atBats = 0 THEN
        p_battingAvg := NULL;
    ELSE
        p_battingAvg := ROUND(p_hits / p_atBats, 3);
    END IF;

    -- Check for division by zero
    IF p_atBats + p_walks_hbp + p_sac = 0 THEN
        p_onBasePercentage := NULL;
    ELSE
        p_onBasePercentage := ROUND((p_hits + p_walks_hbp) / (p_atBats + p_walks_hbp + p_sac), 3);
    END IF;
END myStats;
/
```

# Install Required Python Libraries
- Open a terminal in VS Studio. 
![](assets/2025-10-30-14-55-30.png)

- Click on the terminal dropdown and select git bash as the terminal type. 
![](assets/2025-10-30-14-56-38.png)

- Execute the following commands in your gitbash session to install the required python packages.
```
pip install oracledb
pip install fastmcp
pip install typing
```

- Open the file called .demo_profile file inside your VS Code Directory and update your password, dsn, wallet_location and instant client location. Make sure to save your file once updated. 
```
# Oracle 26ai Autonomous Database Connection Settings
export DB_USER="players"          # Replace with your database username
export DB_PASS="<your pwd>"       # Replace with your database password
export DB_DSN="<your dsn>"        # Replace with your TNS name (e.g., sluggersapex_low)
export WALLET_LOCATION="<your path to wallet>"  # Replace with the full path to your wallet directory ex. C:\Users\Chip Baber\code\db_wallets\Wallet_SluggersAPEX
export INSTANT_CLIENT_DIR="<your instant client dir>" #Replace with path to instant client. ex. C:\Oracle\instantclient-basic-windows.x64-23.9.0.25.07\instantclient_23_9

# Load additional local settings if they exist
if [ -f ~/.bashrc ]; then
   source ~/.bashrc
fi
```

- We are going to slowly build and explain to you the code inside chips_client.py and 26ai_fastmcp.py in the video.

- To add your MCP Server to VS Code:
   - Open the file mcp.json
   - Click add server, select http
   - Paste in your local address. (http://127.0.0.1:8000/mcp)

# Test in VS Code. 

- Click tools to see the current MCP servers. 
   ![](assets/2025-10-27-16-49-18.png)
- View the MCP Server
   ![](assets/2025-10-27-16-49-27.png)
- Type the # in the chat to see your MCP Server
   ![](assets/2025-10-27-16-51-00.png)

- You can select your newly created MCP server and ask a questions via co-pilot to test. Lets test our MCP server and newly created tools now with some questions. 

```
#Get-Table-Column-Comments #Get-Players-AVG-OBP #Get-Players-Stats Describe the AB and H columns in the teamstats table
```
![](assets/2025-11-05-14-54-23.png)


- Now we will get more complex and ask a question that will require the use of all three of our tools. 
```
get all stats for Tank, then calculate his batting average and on base percentage
```
![](assets/2025-11-05-14-55-31.png)

# How do I deploy this on OCI for Multi-Client Use

- The reference architecture below would serve as one possible deployment pattern for your FastMCP deployment. 

[Autoscale a load-balanced web application](https://docs.oracle.com/en/solutions/autoscale-webapp/index.html#GUID-BA16E194-D871-4A39-8385-1CE4A8E6565D)

# Acknowledgement

- I would like to thank https://github.com/brunorsreis for his blog outlining FastMCP and local development against an Oracle Database as inspiration to create this detailed walkthrough. 
