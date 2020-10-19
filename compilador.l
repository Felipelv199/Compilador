%{
#include <stdio.h>
%}
FILE *yyin;

Delim [.,;()\n\t]
PalRes "constantes"|"variables"|"real"|"alfabetico"|"logico"|"entero"|"funcion"|"inicio"|"fin"|"de"|"procedimiento"|"regresa"|"si"|"hacer"|"sino"|"cuando"|"el"|"valor"|"sea"|"otro"|"desde"|"hasta"|"incr"|"decr"|"repetir"|"que"|"mientras"|"se"|"cumpla"|"continua"|"interrumpe"|"limpia (pantalla)"|"lee"|"imprime"|"imprimenl" 

digitos [0-9"."]
alfabeto [A-Za-z]
blank [ \n\t]*
id {alfabeto}+{digitos}* 

tipo ("Entero"|"Flotante"|"real"|"Alfabetico"|"Logico")
Dimens "["({digitos}|{id})"]"(("["({digitos}|{id})"]")?)
GpoId {blank}*{id}({Dimens}?)((:={digitos}*)?){blank}
GpoIds {GpoId}((,{GpoId})*?)

GpoVar {GpoIds}:{tipo};
GpoVars {GpoVar}({GpoVar}*?)
variables variables{GpoVars}

GpoConst {GpoId};
GpoConsts {GpoConst}({GpoConst}*?)
constantes constantes{GpoConsts}
%%
{PalRes} {fprintf(yyout, "%s 						<PalRes>\n",yytext);}
{id} {fprintf(yyout,   "%s 						<Ident>\n",yytext);}
{Delim} {fprintf(yyout,"%s 						<Delim>\n",yytext);}

. ;
%%

int main(int argc, char *argv[])
{
	yyin = fopen(argv[1], "r");
    yyout = fopen("examen.lex", "w"); 
	fprintf(yyout, "---------------------------------------------\n");
	fprintf(yyout, "Lexema					Token\n");
	fprintf(yyout, "---------------------------------------------\n");
	yylex();
	fclose(yyin);
}

int yywrap(){
	return(1);
}