'''
Advanced level guide.
required knowledge: 
    - understanding of basic python: loops, variables etc.
    - basic knowledge of openai platform/api
'''
'''
Welcome to the fast understanding of basic code of AInstein.
In this guide you will learn how to create a basic AI assistant that behaves similar to AInstein, but does not fully replicate it.
Let's start from basic algorithm
'''
'''
         +---------+
         |  start  |
         +----+----+
              |
              v
     +------------------+
     |initialize modules|
     +--------+---------+
              |
              v
     +------------------+
     |  entering a loop |
     +--------+---------+
              |
              | <-----------------------+
              v                         |
    +----------------------+            |
    |listen for audio input|            |
    +--------+-------------+            |
             |                          |
             |                          |
+------------+-------------------+      |
| try to recognize what was said |      |
+------------+-------------------+      |
             |                          |
             v                          |
  +------------------------+            |
  | did we hear something  +------------+
  |     that user said?    |            ^
  +---------+--------------+            |
            |                           |
            v                           |
  +---------------------------+         |
  | send the user request to  |         |
  | OpenAI API and get answer |         |
  +---------+-----------------+         |
            |                           |
            v                           |
     +-----------------+                |
     |  say the answer +----------------+
     +-----------------+
'''