program Test2;
var
   X, A, B, O : integer;
   Z, G, S, P: real;
   T: boolean;
   J: boolean;
   {J: integer;} {J IS ALREADY DECLARED, NOT ALLOWED}

procedure testing();
var
	T: boolean; {T SHOULD BE ALLOWED TO BE DECLARED HERE}
begin
	T := False
end;

begin
   A := 5;
   B := 10;
   G := 6.6;
   S := 10.13
   {M := 20} {M IS NOT DECLARED, SHOULD BE INVALID}
   if (A > B) then
   begin
      X := A;
      A := B;
      B := X
   end
end.	       

