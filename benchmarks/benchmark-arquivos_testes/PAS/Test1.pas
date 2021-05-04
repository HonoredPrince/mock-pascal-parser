program Test1;
   var
      Area, Comprimento, Raio : real; 
   & begin   {O caractere "&" nessa linha deve gerar um erro devido ele ser não conhecido}
      Raio := 4 ;
      Area := 3.14 * Raio * Raio ;
      Comprimento := 2 * 3.14 * Raio 
end.

{Testar multiplos espacos também}
{Gere erros sintáticos, como retirar uma atribuição}
{Veja o que a especificação diz em relação ao uso de ";" no último comando. Eh necessário?}