(* This is an OCaml editor.
   Enter your program here and send it to the toplevel using the "Eval code"
   button or [Ctrl-e]. *)

   type vector = float list;;
   exception DimensionError;;
   exception DivByZeroError;;
   (* let rev (v : vector) : vector = 
     let rec calc list vec = 
       match vec with
       | [] -> list
       | h::t -> calc (h::list) t
     in
     calc [] v
   ;; *)
     
   let v1 = [1.1;2.2;3.3;4.4;5.5] ;;
   let v2 = [6.6;7.7;8.8;9.9;10.10] ;;
   
   let rec create (n : int) (x : float) : vector = 
     if(n<1) then
       raise (DimensionError)
     else  if(n=1)
     then
       [x]
     else
       x :: create (n-1) x
   ;;
   
   (* let dim2 (v : vector) : int  = 
     let acc = 0 in
     let calcLen acc x = acc + 1 in
     let len = List.fold_left calcLen acc v in
     
     len
   ;; *)
   
   let dim (v : vector) : int  =
     
     let rec calc acc vec =
       match vec with
       | [] ->  raise (DimensionError)
       | h :: [] -> acc + 1
       | h :: t -> calc (acc+1) t
     in
     
     calc 0 v
   ;;
   
   let is_zero (v : vector) : bool = 
     
     let rec calc flag v =
       match v with
       | [] -> raise (DimensionError)
       | [0.] -> true
       | 0.::t -> calc flag t
       | h::t -> false
     in
     
     calc true v
   ;;


   let unit (n : int) (j : int) : vector  =
     
     if( j<1 || j>n || n=0)
     then raise (DimensionError)
     else
        let rec calc i j =
          match i with
          | 0 -> []
          | _ -> if(i=n-j+1)
                 then 1. :: calc (i-1) j
                 else 0. :: calc (i-1) j
        in
        calc n j
   ;;  
   
   let rec scale (c : float) (v : vector) : vector  =
     match v with
      | [] -> raise (DimensionError)
      | h::[] -> [c*.h]
      | h::t -> (c*.h) :: scale c t  
   ;;  
   
   (* let addv2 (v1 : vector) (v2 : vector) : vector =
     
     let n = dim v1 in
     let m = dim v2 in
     if(n!=m || n==0 || m == 0)
     then raise (DimensionError)
     else
       let rec calc list v1 v2 = 
         match v1,v2 with
         | [],[] -> list
         | h1::t1 , h2::t2 -> calc ((h1+.h2)::list) t1 t2
         | _ -> raise (DimensionError)
       in
       rev (calc [] v1 v2)
   ;;
    *)
  let rec addv (v1 : vector) (v2 : vector) : vector = 
      match v1,v2 with
      | [],[] -> raise (DimensionError)
      | h1::[],h2::[] -> [h1+.h2]
      | h1::t1,h2::t2 -> if(dim v1 != dim v2)
                         then raise (DimensionError)
                         else (h1+.h2) :: addv t1 t2
      | _ -> raise (DimensionError) 
                            

   let rec dot_prod (v1 : vector) (v2 : vector) : float =
     match v1,v2 with
     | [] , [] -> raise DimensionError
     | h1::[],h2::[] -> h1*.h2
     | h1::t1,h2::t2 -> h1*.h2 +. dot_prod t1 t2
     | _ -> raise DimensionError
   
       
   let rec inv (v : vector) : vector = 
     match v with
      | [] -> raise (DimensionError)
      | h::[] -> [-.h]
      | h::t -> (-.h) :: inv t
   ;;
   
   let length (v : vector) : float = 
     
     if(dim v < 1)
     then raise (DimensionError)
     else
     let m = dot_prod v v
     in
     sqrt(m)
   ;;
   
   let angle (v1 : vector) (v2 : vector) : float =
     
     let n = dim v1 in
     let m = dim v2 in
     if(n!=m || n=0 || m=0)
     then raise (DimensionError)
     else
      let lv1 = length v1 in
      let lv2 = length v2 in
      if(lv1 = 0. || lv2 = 0.)
      then raise (DivByZeroError)
      else
       let temp = (dot_prod v1 v2)/.((lv1)*.(lv2))
       in acos (temp);;
    
(*
################################################################################  
                                  Test cases   
################################################################################
*)

(* Wrap each test function in try/with to avoid termination on DimensionError *)

let test_create n x =
  try
    let v = create n x in
    Printf.printf "create(%d, %0.2f) -> " n x;
    List.iter (Printf.printf "%0.2f ") v;
    print_newline ();
  with DimensionError ->
    Printf.printf "create(%d, %0.2f) -> DimensionError\n" n x;;

let test_dim v =
  try
    Printf.printf "dim(";
    List.iter (Printf.printf "%0.2f;") v;
    Printf.printf ") -> %d\n" (dim v);
  with DimensionError ->
    Printf.printf "dim(...) -> DimensionError\n";;

let test_is_zero v =
  try
    Printf.printf "is_zero(";
    List.iter (Printf.printf "%0.2f;") v;
    Printf.printf ") -> %b\n" (is_zero v);
  with DimensionError ->
    Printf.printf "is_zero(...) -> DimensionError\n";;

let test_unit n j =
  try
    let v = unit n j in
    Printf.printf "unit(%d, %d) -> " n j;
    List.iter (Printf.printf "%0.2f ") v; 
    print_newline ();
  with DimensionError ->
    Printf.printf "unit(%d, %d) -> DimensionError\n" n j;;

let test_scale c v =
  try
    let r = scale c v in
    Printf.printf "scale(%0.2f, [" c;
    List.iter (Printf.printf "%0.2f;") v;
    Printf.printf "]) -> ";
    List.iter (Printf.printf "%0.2f ") r;
    print_newline ();
  with DimensionError ->
    Printf.printf "scale(%0.2f, [...]) -> DimensionError\n" c;;

let test_addv v1 v2 =
  try
    let r = addv v1 v2 in
    Printf.printf "addv(["; List.iter (Printf.printf "%0.2f;") v1;
    Printf.printf "], ["; List.iter (Printf.printf "%0.2f;") v2;
    Printf.printf "]) -> ";
    List.iter (Printf.printf "%0.2f ") r;
    print_newline ();
  with DimensionError ->
    Printf.printf "addv(...) -> DimensionError\n";;

let test_dot_prod v1 v2 =
  try
    let d = dot_prod v1 v2 in
    Printf.printf "dot_prod(["; List.iter (Printf.printf "%0.2f;") v1;
    Printf.printf "], ["; List.iter (Printf.printf "%0.2f;") v2;
    Printf.printf "]) -> %0.2f\n" d;
  with DimensionError ->
    Printf.printf "dot_prod(...) -> DimensionError\n";;

let test_inv v =
  try
    let r = inv v in
    Printf.printf "inv([";
    List.iter (Printf.printf "%0.2f;") v;
    Printf.printf "]) -> ";
    List.iter (Printf.printf "%0.2f ") r;
    print_newline ();
  with DimensionError ->
    Printf.printf "inv([...]) -> DimensionError\n";;

let test_length v =
  try
    Printf.printf "length([";
    List.iter (Printf.printf "%0.2f;") v;
    Printf.printf "]) -> %0.2f\n" (length v);
  with DimensionError ->
    Printf.printf "length([...]) -> DimensionError\n";;

let test_angle v1 v2 =
  try
    Printf.printf "angle([";
    List.iter (Printf.printf "%0.2f;") v1;
    Printf.printf "], [";
    List.iter (Printf.printf "%0.2f;") v2;
    Printf.printf "]) -> %0.2f radians\n" (angle v1 v2);
  with 
   | DimensionError -> Printf.printf "angle([...]) -> DimensionError\n"
   | DivByZeroError -> Printf.printf "angle([...]) -> DivByZeroError\n";;
  ;;

Printf.printf "\n-- create tests --\n";;
test_create 3 2.0;;
test_create 1 3.14;;
test_create (-1) 5.0;;  (* should raise DimensionError *)
test_create 100 11.17;;
test_create 0 0.0;;  (* should raise DimensionError *)

(* Test Cases for dim (vector -> int) *)
Printf.printf "\n-- dim tests --\n";;
test_dim [1.0; 2.0; 3.0];;
test_dim [0.0];;
test_dim [];   (* should it raise error for empty vector? If so, dimension error *)
test_dim [5.0; 5.0];;
test_dim (create 100 1.0);;

(* Test Cases for is_zero (vector -> bool) *)
Printf.printf "\n-- is_zero tests --\n";;
test_is_zero [0.0; 0.0; 0.0];;
test_is_zero [1.0; 0.0; 0.0];;
test_is_zero [0.0];;
test_is_zero [2.0; 2.0];;
test_is_zero (unit 5 3);;
test_is_zero ([]);;

(* Test Cases for unit (int -> int -> vector) *)
Printf.printf "\n-- unit tests --\n";;
test_unit 3 1;;
test_unit 3 3;;
test_unit 5 2;;
test_unit 4 5;;  (* should raise DimensionError if j=5 > n=4 *)

(* Test Cases for scale (float -> vector -> vector) *)
Printf.printf "\n-- scale tests --\n";;
test_scale 2.0 [1.0; 2.0; 3.0];;
test_scale 0.0 [1.0; 2.0];;
test_scale (-1.0) [1.0; -2.0];;
test_scale 1.0 [];;
test_scale 0.0 [1.;2.;3.;4.;5.];;

(* Test Cases for addv (vector -> vector -> vector) *)
Printf.printf "\n-- addv tests --\n";;
test_addv [1.0; 2.0] [3.0; 4.0];;
test_addv [3.0; 4.0] [1.0; 2.0];;  (* Commutativity *)
test_addv [0.;0.;0.;0.;0.;0.;0.;0.] [1.;2.;3.;4.;5.;6.;7.;8.];; (* Identity *)
test_addv [0.0; 0.0] [0.0; 0.0];;
test_addv [1.0; 2.0; 3.0] [1.0; 2.0];  (* dimension mismatch *)
test_addv [] [];;

(* Test Cases for dot_prod (vector -> vector -> float) *)
Printf.printf "\n-- dot_prod tests --\n";;
test_dot_prod [1.0; 2.0; 3.0] [4.0; 5.0; 6.0];;
test_dot_prod [1.0] [2.0];;
test_dot_prod [1.0; 2.0] [3.0];  (* mismatch *)
test_dot_prod [0.;0.;0.;0.;0.;0.;0.;0.] [1.;2.;3.;4.;5.;6.;7.;8.];; (* Dimnishing Property *)
test_dot_prod [] [];;

(* Test Cases for inv (vector -> vector) *)
Printf.printf "\n-- inv tests --\n";;
test_inv [1.0; -2.0; 3.0];;
test_inv [0.0; 0.0];;
test_inv [5.0];;
test_inv [];;

(* Test Cases for length (vector -> float) *)
Printf.printf "\n-- length tests --\n";;
test_length [3.0; 4.0];;
test_length [0.0; 0.0; 0.0];;
test_length [5.0];;
test_length (create 100 5.);;
test_length [];;

(* Test Cases for angle (vector -> vector -> float) *)
Printf.printf "\n-- angle tests --\n";;
test_angle [1.0; 0.0] [0.0; 1.0];;
test_angle [1.0; 1.0] [1.0; 1.0];;
test_angle [1.0; 2.0] [2.0; 6.0; 8.0]; (* mismatch *)
test_angle [2.0; -4.0] [-1.0; 2.0];;
test_angle [0.0; 0.0] [0.0; 0.0];;

(*
################################################################################  
                              PROOFS   
################################################################################


For all vectors u, v, and w, and for all scalars b and c:

    (Commutativity)  u + v = v + u
    (Associativity) u + (v + w) = (u + v) + w
    (Identity of addition)  v + O = v
    (Identity scalar)  1.v = v
    (Annihilator scalar)  0.v = O
    (Additive Inverse)  v + (- v) = O
    (Scalar product combination)  b.(c.v) = (b.c).v
    (Scalar sum-product distribution)  (b + c).v = b.v + c.v
    (Scalar Distribution over vector sums)  b.(u + v) = b.u + b.v

    PROOF 1) Commutativity of addv function:
    To show that addv is commutative, we need to show that for all vectors u and v of dim = n, addv u v = addv v u.
    Proof: By induction on the dimension of vectors u and v.
    
    Predicate P(n) : For all vectors u and v of dim = n, addv u v = addv v u.

    Base case: If u and v are both vectors of dim = 1, then addv u v = [u1 + v1] = [v1 + u1] = addv v u. (By function definition and commutativity of float addition)

    Inductive step: Suppose addv u v = addv v u for all vectors u and v of dimension k.
    Let u be a vector of dimension k+1 and v be a vector of dimension k+1.
    then by function definition, add v u will be matched with the case h1::t1, h2::t2 
    where h1 and h2 are the first elements of u and v respectively and t1 and t2 are the rest of the vectors of  dim = k,
    then addv u v = (h1 + h2) :: addv t1 t2 .
    By induction hypothesis, addv t1 t2 = addv t2 t1.
    By float addition commutativity, h1 + h2 = h2 + h1.
    Therefore, addv u v = (h1 + h2) :: addv t1 t2 = (h2 + h1) :: addv t2 t1 = addv v u.
    Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
    Therefore, by induction, P(n) is true for all n >= 1.






    PROOF 2) Associativity of addv function:
    To show that addv is associative, we need to show that for all vectors u, v, and w of dim = n, addv u (addv v w) = addv (addv u v) w.
    Proof: By induction on the dimension of vectors u, v, and w.

    Predicate P(n) : For all vectors u, v, and w of dim = n, addv u (addv v w) = addv (addv u v) w.

    Base case: If u, v, and w are all vectors of dim = 1 (let v = [v1] , w = [w1] , u = [u1]), then addv u (addv v w) = add u ([v1 + w1]) = [u1 + v1 + w1] (By function definition)  
    and addv (addv u v) w = addv ([u1 + v1]) w = [u1 + v1 + w1] (By function definition)
    By float addition associativity, u1 + v1 + w1 = u1 + (v1 + w1) = (u1 + v1) + w1.
    Therefore, addv u (addv v w) = addv (addv u v) w.

    Induction step: Suppose addv u (addv v w) = addv (addv u v) w for all vectors u, v, and w of dimension k.
    Let u be a vector of dimension k+1 and v be a vector of dimension k+1 and w be a vector of dimension k+1.
    then by function definition, addv v w will be matched with the -=-0e h1::t1, h2::t2 
    where h1 and h2 are the first elements of v and w respectively and t1 and t2 are the rest of the vectors of  dim = k,
    then addv u (addv v w) = addv u ((h1 + h2) :: addv t1 t2) 

    Let h3 be the first element of u and t3 be the rest of the vect,or of dim = k.
    then addv u ((h1 + h2) :: addv t1 t2) = (h3 + (h1 + h2)) :: addv t3 (addv t1 t2) 
    = (h3 + (h1 + h2)) :: addv t3 (addv t1 t2) {By function definition and float addition associativity}

    By induction hypothesis, addv t3 (addv t1 t2) = addv (addv t3 t1) t2.
    Therefore, 
    
    addv (addv u v) w = addv ((h3 + h1) :: addv t3 t1) w 
    = ((h3 + h1) + h2) :: addv (addv t3 t1) t2 { By function definition } 
    = (h3 + (h1 + h2)) :: addv (addv t3 t1) t2 { By float addition associativity }
    = (h3 + (h1 + h2)) :: addv t3 (addv t1 t2) { By induction hypothesis }
    = addv u (addv v w).
    Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
    Therefore, by induction, P(n) is true for all n >= 1.

     
  PROOF 3) Identity of addition:
  To show that for all vectors v of dim = n, addv v O = v (where O represents zero vector of dim = n).

  Proof: By induction on the dimension of vector v.

  Predicate P(n) : For all vectors v of dim = n, addv v O = v.

  Base case: If v is a vector of dim = 1, then addv v O = [v1 + 0] = [v1] = v. (By function definition and float addition identity)

  Inductive step: Suppose addv v O = v for all vectors v of dimension k.
  Let v be a vector of dimension k+1.
  then by function definition, addv v O will be matched with the case h1::t1, h2::t2 
  where h1 and h2 are the first elements of v and O respectively and t1 and t2 are the rest of the vectors of  dim = k,
  then addv v O = (h1 + h2) :: addv t1 t2 
  = (h1 + h2) :: t1 {By induction hypothesis as t2 is zero vector of dim = k}
  = h1 :: t1 {By float addition identity as h2 = 0}
  = v.

  Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
  Therefore, by induction, P(n) is true for all n >= 1.





  PROOF 4) Identity scalar:
  To show that for all vectors v of dim = n, scale 1.0 v = v.

  Proof: By induction on the dimension of vector v.

  Predicate P(n) : For all vectors v of dim = n, scale 1.0 v = v.

  Base case: If v is a vector of dim = 1, then scale 1.0 v = [1.0 * v1] = [v1] = v. (By function definition and float multiplication identity)

  Inductive step: Suppose scale 1.0 v = v for all vectors v of dimension k.
  Let v be a vector of dimension k+1.
  then by function definition, scale 1.0 v will be matched with the case h::t 
  where h is the first element of v and t is the rest of the vectors of  dim = k,
  then scale 1.0 v = (1.0 * h) :: scale 1.0 t
  = h :: t {By induction hypothesis}
  = v.

  Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
  Therefore, by induction, P(n) is true for all n >= 1.



  PROOF 5) Annihilator scalar:
  To show that for all vectors v of dim = n, scale 0.0 v = O (where O represents zero vector of dim = n).

  Proof: By induction on the dimension of vector v.

  Predicate P(n) : For all vectors v of dim = n, scale 0.0 v = O.

  Base case: If v is a vector of dim = 1, then scale 0.0 v = [0.0 * v1] = [0.0] = O. (By function definition and float multiplication identity)

  Inductive step: Suppose scale 0.0 v = O for all vectors v of dimension k.
  Let v be a vector of dimension k+1.
  then by function definition, scale 0.0 v will be matched with the case h::t 
  where h is the first element of v and t is the rest of the vectors of  dim = k,
  then scale 0.0 v = (0.0 * h) :: scale 0.0 t
  = 0.0 :: scale 0.0 t {By float multiplication identity}
  = 0.0 :: o {By induction hypothesis (o represents zero vector of dim = k)}
  = O.

  Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
  Therefore, by induction, P(n) is true for all n >= 1.



  PROOF 6) Additive Inverse:
  To show that for all vectors v of dim = n, addv v (-v) = O (where O represents zero vector of dim = n).

  Proof: By induction on the dimension of vector v.

  Predicate P(n) : For all vectors v of dim = n, addv v (-v) = O.

  Base case: If v is a vector of dim = 1, then addv v (-v) = [v1 + (-v1)] = [0.0] = O. (By function definition and float addition inverse)

  Inductive step: Suppose addv v (-v) = O for all vectors v of dimension k.

  Let v be a vector of dimension k+1.
  then by function definition, addv v (-v) will be matched with the case h::t 
  where h is the first element of v and t is the rest of the vectors of  dim = k,
  then addv v (-v) = (h + (-h)) :: addv t (-t)
  = 0.0 :: addv t (-t) {By float addition inverse}
  = 0.0 :: o {By induction hypothesis (o represents zero vector of dim = k)}
  = O.

  Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
  Therefore, by induction, P(n) is true for all n >= 1.

  PROOF 7) Scalar product combination:
  To show that for all vectors v of dim = n and scalars b and c, scale b (scale c v) = scale (b * c) v.

  Proof: By induction on the dimension of vector v.

  Predicate P(n) : For all vectors v of dim = n and scalars b and c, scale b (scale c v) = scale (b * c) v.

  Base case: If v is a vector of dim = 1, then (let v = [v1]) 
    scale b (scale c v) 
  = scale b [c * v1] {By function definition}
  = [b * (c * v1)]   {By function definition}
  = [(b * c) * v1]    {By float multiplication associativity}
  = scale (b * c) v.  {By function definition}

  Inductive step: Suppose scale b (scale c v) = scale (b * c) v for all vectors v of dimension k.

  Let v be a vector of dimension k+1.
  then by function definition, scale b (scale c v) will be matched with the case h::t 
  where h is the first element of v and t is the rest of the vectors of  dim = k,
  then scale b (scale c v)
  = scale b (scale c h::t) {By function definition}
  = scale b ((c * h) :: (scale c t)) {By function definition}
  = (b * (c * h)) :: scale b (scale c t) {By function definition}
  = (b * (c * h)) :: scale (b * c) t {By induction hypothesis}
  = scale (b * c) h::t {By function definition}
  = scale (b * c) v. {By function definition}

  Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
  Therefore, by induction, P(n) is true for all n >= 1.


  PROOF 8) Scalar sum-product distribution:
  To show that for all vectors v of dim = n and scalars b and c, scale (b + c) v = addv (scale b v) (scale c v).
  
  Proof: By induction on the dimension of vector v.

  Predicate P(n) : For all vectors v of dim = n and scalars b and c, scale (b + c) v = addv (scale b v) (scale c v).

  Base case: If v is a vector of dim = 1, then (let v = [v1]) 
    scale (b + c) v 
    = [v1 * (b + c)] {By function definition}
    = [v1 * b + v1 * c] {By float multiplication distributivity}
    
    Also, addv (scale b [v1]) (scale c [v1])
    = addv [v1 * b] [v1 * c] {By function definition of scale}
    = [v1 * b + v1 * c] {By function definition of addv}

    Therefore, P(1) = True.

  Inductive step: Suppose scale (b + c) v = addv (scale b v) (scale c v) for all vectors v of dimension k.
  Let v be a vector of dimension k+1.
  then by function definition, scale (b + c) v will be matched with the case h::t 
  where h is the first element of v and t is the rest of the vector of  dim = k,
  then scale (b + c) v
  = scale (b + c) h::t 
  = ((b + c) * h) :: scale (b + c) t {By function definition}
  = ((b * h) + (c * h)) :: scale (b + c) t {By float multiplication distributivity}
  = ((b * h) + (c * h)) :: addv (scale b t) (scale c t) {By induction hypothesis}


  Also,  addv (scale b v) (scale c v). {By decomposition of v}
  = addv (scale b h::t) (scale c h::t) {By function definition}
  = ((h1*b) :: scale b t1) ((h2*b) :: scale b t2) {By function definition of scale}
  = ((h1*b) + (h2*b)) :: addv (scale b t1) (scale c t2) {By function definition of addv}
  = (b * (h1 + h2)) :: addv (scale b t1) (scale c t2) {By float multiplication distributivity}

  Therefore, scale (b + c) v = addv (scale b v) (scale c v).
  
  Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
  Therefore, by induction, P(n) is true for all n >= 1.


  PROOF 9) Scalar Distribution over vector sums:
  To show that for all vectors u and v of dim = n and scalar b, scale b (addv u v) = addv (scale b u) (scale b v).

  Proof: By induction on the dimension of vectors u and v.

  Predicate P(n) : For all vectors u and v of dim = n and scalar b, scale b (addv u v) = addv (scale b u) (scale b v).

  Base case: If u and v are both vectors of dim = 1, then (let u = [u1] and v = [v1]) 
    scale b (addv u v) 
    = scale b [u1 + v1] {By function definition}
    = [b * (u1 + v1)] {By function definition}
    = [b * u1 + b * v1] {By float multiplication distributivity}
    
    Also, addv (scale b u) (scale b v)
    = addv [u1 * b] [v1 * b] {By function definition of scale}
    = [u1 * b + v1 * b] {By function definition of addv}

    Therefore, P(1) = True.

  Inductive step: Suppose scale b (addv u v) = addv (scale b u) (scale b v) for all vectors u and v of dimension k.
  Let u be a vector of dimension k+1 and v be a vector of dimension k+1.
  then by function definition, scale b (addv u v) will be matched with the case h1::t1, h2::t2 
  where h1 and h2 are the first elements of u and v respectively and t1 and t2 are the rest of the vectors of  dim = k,
  then scale b (addv u v)
  = scale b (addv h1::t1 h2::t2) {By function definition}
  = scale b ((h1 + h2) :: addv t1 t2) {By function definition}
  = (b * (h1 + h2)) :: scale b (addv t1 t2) {By function definition}
  = (b * (h1 + h2)) :: addv (scale b t1) (scale b t2) {By induction hypothesis}
  
  Also, addv (scale b u) (scale b v)
  = addv (scale b h1::t1) (scale b h2::t2) {By decomposition of u and v}
  = addv ((h1*b) :: scale b t1) ((h2*b) :: scale b t2) {By function definition of scale}
  = ((h1*b) + (h2*b)) :: addv (scale b t1) (scale b t2) {By function definition of addv}
  = (b * (h1 + h2)) :: addv (scale b t1) (scale b t2) {By float multiplication distributivity}

  Therefore, scale b (addv u v) = addv (scale b u) (scale b v).

  Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
  Therefore, by induction, P(n) is true for all n >= 1.


################################################################################  
                          ADDITIONAL PROPERTIES   
################################################################################

1) Dot product Commutativity: 
To show that for all vectors u and v, dot_prod u v = dot_prod v u.

Proof: By Induction on the dimension of vectors u and v.

Predicate P(n) : For all vectors u and v of dim = n, dot_prod u v = dot_prod v u.

Base case: If u and v are both vectors of dim = 1, then (let u = [u1] and v = [v1]) 
  dot_prod u v 
  = u1 * v1 {By function definition of dot_prod} 
  = v1 * u1 {By float multiplication commutativity}
  = dot_prod v u. {By inverse of function definition of dot_prod}

  Therefore, P(1) = True.

Inductive step: Suppose dot_prod u v = dot_prod v u for all vectors u and v of dimension k.
Let u be a vector of dimension k+1 and v be a vector of dimension k+1.
then by function definition, dot_prod u v will be matched with the case h1::t1, h2::t2 
where h1 and h2 are the first elements of u and v respectively and t1 and t2 are the rest of the vectors of  dim = k,
then dot_prod u v 
= (h1 * h2) + dot_prod t1 t2. {By function definition of dot_prod}
= (h2 * h1) + dot_prod t2 t1. {By induction hypothesis}

Also, dot_prod v u
= (h2 * h1) + dot_prod t2 t1. {By function definition of dot_prod}

Therefore, dot_prod u v = dot_prod v u.

Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
Therefore, by induction, P(n) is true for all n >= 1.



2) Length of a vector is equal to length of it's inverse:
To show that for all vectors v, length v = length (inv v).

Proof: By Induction on the dimension of vector v.

Predicate P(n) : For all vectors v of dim = n, length v = length (inv v).

Base case: If v is a vector of dim = 1, then (let v = [v1]) 
  length v 
  = sqrt(v1 * v1) {By function definition of length} 
  = |v1| {By definition of square root}

  Also, length (inv v)
  = length [-v1] {By function definition of inv}
  = sqrt((-v1) * (-v1)) {By function definition of length}
  = sqrt(v1 * v1) {As (-v1) * (-v1) = v1 * v1 because of float multiplication associativity as -1*-1 = 1}
  = |v1| {By definition of square root}

  Therefore, P(1) = True.

  Inductive step: Suppose length v = length (inv v) for all vectors v of dimension k.
  Let v be a vector of dimension k+1.
  then by function definition, length v will be matched with the case h::t 
  where h is the first element of v and t is the rest of the vectors of  dim = k,
  then length v
  = sqrt(h * h + length t * length t) {By function definition of length}

  I used the following property that for all vectors u dot_prod u u = length u * length u.
  (As my length function is defined as sqrt(dot_prod u u), so this property holds)

  Also, length (inv v)
  = sqrt((-h) * (-h) + length (inv t) * length (inv t)) {By function definition of inv and length}
  = sqrt(h * h + length t * length t) {By float multiplication associativity as -1*-1 = 1}

  Therefore, length v = length (inv v).

  Hence, P(k) => P(k+1) (Not really implies but still we can write this) for all k >=1 and P(1) = True.
  Therefore, by induction, P(n) is true for all n >= 1.


3) Dot product with scale:
To show that for all vectors u and v and scalar b, dot_prod (scale b u) v = b * dot_prod u v.

Proof: By Induction on the dimension of vectors u and v.

Predicate P(n) : For all vectors u and v of dim = n and scalar b, dot_prod (scale b u) v = b * dot_prod u v.

Base Case : If u and v are both vectors of dim = 1, then (let u = [u1] and v = [v1]) 
  dot_prod (scale b u) v 
  = dot_prod [b * u1] [v1] {By function definition of scale}
  = (b * u1) * v1 {By function definition of dot_prod}
  = b * (u1 * v1) {By float multiplication associativity}
  = b * dot_prod u v. {By inverse of function definition of dot_prod}

  Therefore, P(1) = True.

Inductive step: Suppose dot_prod (scale b u) v = b * dot_prod u v for all vectors u and v of dimension k.
Let u be a vector of dimension k+1 and v be a vector of dimension k+1.
then by function definition, dot_prod (scale b u) v will be matched with the case h1::t1, h2::t2 
where h is the first element of u and v respectively and t1 and t2 are the rest of the vectors of  dim = k,
then dot_prod (scale b u) v
= dot_prod ((b*h1) :: scale b t1) h2::t2 {By function definition of scale}
= (b*h1) * h2 + dot_prod (scale b t1) t2 {By function definition of dot_prod}
= b * (h1 * h2) + b * dot_prod t1 t2 {By induction hypothesis}
= b * (h1 * h2 + dot_prod t1 t2) {By float multiplication distributivity}
= b * dot_prod (h1::t1) (h2::t2) {By inverse of function definition of dot_prod}
= b * dot_prod u v.

Therefore, dot_prod (scale b u) v = b * dot_prod u v.

Hence, P(k) => P(k+1) for all k >=1 and P(1) = True.
Therefore, by induction, P(n) is true for all n >= 1.


4) Angle between vector and it's inverse is always pi:
To show that for all vectors v, angle v (inv v) = pi.

Proof: Consider a vector v of dim = n(>=1).


angle v (inv v) = acos(dot_prod v (inv v) / (length v * length (inv v))) {By function definition of angle}
= acos(dot_prod v (inv v) / (length v * length v)) {As length v = length (inv v) (Proved above)}
= acos(dot_prod v (inv v) / (dot_prod v v)) {As length v = sqrt(dot_prod v v) by definition of length}
= acos(dot_prod v (-v) / (dot_prod v v)) {By the property v + (inv v) = O (Proved earlier)}
= acos(-dot_prod v v / (dot_prod v v)) {By the property dot_prod (scale a v) u = a*dot_prod v u (Proved above)}
= acos(-1) {By float division}
= pi. {By definition of acos}

Therefore, angle v (inv v) = pi.


*)


