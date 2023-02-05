# Volleyball Dashboard

# Objective
Interactive dashboard to visualize volleyball data and statistics to improve performance

Website: https://vball-dashboard.onrender.com/
Demo: https://vball-dashboard.onrender.com/example

# How To Use
File must be of type, .CSV
CSV formatting should at least contain the following 4 features, attributes, or headings: 'Player', 'Set', 'Event', and 'Location' in any order

## Data Feature Definitions
**Player**
Name of player, e.g., Donald, John, Taylor Crabb

**Set**
Set number, e.g., 1, 4, 10, 999
*set numbers were designed to be continuous, e.g., sets 1-3 could be from a tournament, and sets 4-8 could be from practice games

**Event**
Offensive or defensive play for a given player and set number, e.g., dig, hard driven, tool

**Location**
Location: integer court location of offensive or defense play where applicable, e.g., 1, 2, 3, 4, 5, or 6

## Recording Data
Record events for each set and player that you want to track, e.g., 'block' for Ben on set number 42

**Offense**
Offensive events can consist of any of the following: 'hard driven', 'hit shank', 'roll shot', 'tip', 'block kill', 'cut shot', 'touch', 'block shank', 'tool'
Any unsuccessful kills can be labled as attempts, e.g., 'hitting attempt', for use in hitting percentage calculations

**Defense**
Record digs for a particular player, set, and location

**When and how to record court location**
Court locations for offense should be based on the court opposite from the player attacking, while court locations for defensive events should be based on the court side of the playing defending

Intent of locations was designed to capture offensive/defensive events that land on the court, e.g., hard driven spike to court location 5 or dig at court location 2. Some offensive hits like 'hit shank' or 'block shank' may not be recorded depending on the user recording the data

