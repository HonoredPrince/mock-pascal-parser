program Test2;
var
   X, A, B, O : integer;
   Z, G, S, P: real;
begin
   A := 5;
   B := 10;
   G := 6.6;
   S := 10.13;
   if (A > B) then
   begin
      X := A;
      A := B;
      B := X;
      O := G + A {INTERGER := REAL + INTERGER SHOULD BE INVALID}
   end
end.	       

