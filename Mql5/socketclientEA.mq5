//+------------------------------------------------------------------+
//|                                               socketclientEA.mq5 |
//|                        Copyright 2018, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2018, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
#include<Trade\Trade.mqh>
CTrade trade;

long timerCount = 0;
sinput int lrlenght = 1;
int socket;
string open_symbols[]; 



int OnInit() {
 EventSetTimer(5); 
 socket=SocketCreate();
 return(INIT_SUCCEEDED); }

void OnDeinit(const int reason) {
 SocketClose(socket); }

void OnTimer() {
 socket=SocketCreate();
 if(socket!=INVALID_HANDLE) {
  if(SocketConnect(socket,"localhost",7000,1000)) {
   Print("Connected to "," localhost",":",7000);
         
   double clpr[];
   int copyed = CopyClose(_Symbol,PERIOD_CURRENT,0,lrlenght,clpr);
         
   string tosend;
   for(int i=0;i<ArraySize(clpr);i++) 
      tosend+=(string)clpr[i]+" ";
             
   string received = socksend(socket, tosend) ? socketreceive(socket, 10000) : ""; 
   Print(received);
   
   executeOrder(received);
   //Comment("1 ----->", received);
   //int Size=ArraySize(received);
   //Print(Size);
   

   }
   
  //else Print("Connection ","localhost",":",7000," error ",GetLastError());
  SocketClose(socket); }
 else Print("Socket creation error ",GetLastError());
 //PrintFormat("%s(): timerCount [%d]", __FUNCTION__, timerCount++); 
 }



bool socksend(int sock,string request) {
 char req[];
 int  len=StringToCharArray(request,req)-1;
 if(len<0) return(false);
 return(SocketSend(sock,req,len)==len); }
  
  
  
string socketreceive(int sock, int timeout) {
 char rsp[];
 string result = "";
 uint len;
 uint timeout_check=GetTickCount()+timeout;
 do {  
  len=SocketIsReadable(sock);
  //Print(len); 
  if(len) {
   int rsp_len;
   rsp_len = SocketRead(sock,rsp,len,timeout);
   //Print(rsp_len);
   if(rsp_len>0) {
   result+=CharArrayToString(rsp,0,rsp_len); } }
  } while((GetTickCount()<timeout_check) && !IsStopped());
 return result; }
 
 
 void executeOrder(string values){
  string res[];
  StringSplit(values, ',', res);
  int Size=ArraySize(res);
  Print(Size); 
  
  if(Size>0){
     string trading_info = "";

     for(int i=0; i<Size-1; i=i+4){
       //Print(res[i], res[i+1], res[i+2]);
       string symbol = res[i];
       string orderType = res[i+1];
       double recevedExecuteTime = StringToDouble(res[i+2]);
       string position = res[i+3];
       
       //Print(symbol); 
       //Print(orderType); 
       //Print(recevedExecuteTime);
       //Print(position);
       //Sleep(10000);
       string dtemp = accountInfo();
       //trading_info += (symbol +": "+orderType +", " +string(recevedExecuteTime) +"\n");      
       //Comment(dtemp+"TRADING INFORMATION:"+ "\n\n" +"Order Placeing" +"\n" +"____________________" +"\n" +trading_info);
       Comment(dtemp);

       //Trades open,close function
       trade_open_close(symbol, orderType, position);
      
       
       }
   }
   else{
       string dtemp = accountInfo();
       Comment(dtemp);
    }
 

  }
 
void trade_open_close(string symbol,string orderType,string position)
  {
      //open trades
      if(position == "open"){        
        if(orderType == "buy"){
            double Ask=NormalizeDouble(SymbolInfoDouble(symbol,SYMBOL_ASK),_Digits);
            trade.Buy(0.01,symbol,Ask,0,NULL,NULL);}
            
         if(orderType == "sell"){
            double Bid = NormalizeDouble(SymbolInfoDouble(_Symbol, SYMBOL_BID), _Digits);
            trade.Sell(0.01,symbol,Bid,0,NULL,NULL);}
       }
       
       //close trades
       if(position == "close"){
         trade.PositionClose(symbol);}

  } 
 
 

  
string accountInfo(){
    string temp =(
    "------------------------------------------------\n"
    + "ACCOUNT INFORMATION:\n"
    + "\n"
    + "Account Name:     " + AccountInfoString(ACCOUNT_NAME)+ "\n"
    + "Broker Name:     " + AccountInfoString(ACCOUNT_COMPANY)+ "\n"
    + "Server Name:     " + AccountInfoString(ACCOUNT_SERVER)+ "\n"
    + "Currency:     " + AccountInfoString(ACCOUNT_CURRENCY)+ "\n"
    + "Account Leverage:     " + IntegerToString(AccountInfoInteger(ACCOUNT_LEVERAGE))+ "\n"
    + "Account Balance:     " + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE))+ "\n"
    + "Account Equity:     " + DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY))+ "\n"
    + "Free Margin:     " + DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_FREE))+ "\n"
    + "Margin Level:     " + DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_LEVEL))+ "\n"
    + "Account Profit:     " + DoubleToString(AccountInfoDouble(ACCOUNT_PROFIT))+ "\n\n"
    + "------------------------------------------------\n"
    );
    return temp;
 }
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 