%% Initial state
wall(0, _).
wall(_, 0).
wall(5, _).
wall(_, 5).
wumpus(1, 3, 0).
pit(3, 3).
pit(3, 1).
pit(4, 4).
at(1, 1, 0).
orientation(0, 0).
gold(2, 3).
status(0).

%% Statuses
status(S) :- SP is S - 1, result(a, SP).

%% Basic movement rules
orientation(O, S) :- SP is S - 1, OP is (O - 1) mod 3, status(SP), orientation(OP, SP).
at(X, Y, S) :- SP is S - 1, forward(SP), XP is X - 1, at(XP, Y, SP), orientation(0, SP).
at(X, Y, S) :- SP is S - 1, forward(SP), YP is Y - 1, at(X, YP, SP), orientation(1, SP).
at(X, Y, S) :- SP is S - 1, forward(SP), XP is X + 1, at(XP, Y, SP), orientation(2, SP).
at(X, Y, S) :- SP is S - 1, forward(SP), YP is Y + 1, at(X, YP, SP), orientation(3, SP).

%% Derived table state
stentch(X, Y, S) :- XP is X - 1, wumpus(XP, Y, S).
stentch(X, Y, S) :- XP is X + 1, wumpus(XP, Y, S).
stentch(X, Y, S) :- YP is Y + 1, wumpus(X, YP, S).
stentch(X, Y, S) :- YP is Y - 1, wumpus(X, YP, S).
breeze(X, Y) :- XP is X - 1, pit(XP, Y).
breeze(X, Y) :- XP is X + 1, pit(XP, Y).
breeze(X, Y) :- YP is Y + 1, pit(X, YP).
breeze(X, Y) :- YP is Y - 1, pit(X, YP).


%% Actions classification
mortal_item(X, Y, S) :- at(X, Y, S), wumpus(X, Y, S).
mortal_item(X, Y, S) :- at(X, Y, S), pit(X, Y).
danger(X, Y, S) :- at(X, Y, S), stentch(X, Y, S).
danger(X, Y, S) :- at(X, Y, S), breeze(X, Y).
ok(X, Y, S) :- not(mortal_item(X, Y, S)), not(danger(X, Y, S)).
dead(X, Y, S) :- at(X, Y, S), mortal_item(X, Y, S).
hold_gold(S) :- SP is S - 1, hold_gold(SP).
hold_gold(S) :- at(X, Y, S), gold(X, Y).
win(S) :- hold_gold(S), at(1, 1, S).
fired(S) :- SP is S - 1, not(fired(SP)), stentch(X, Y, SP).
wumpus(X, Y, S) :- SP is S - 1, wumpus(X, Y, SP), not(wumpus_killed(S)).
wumpus_killed(S) :- at(X, Y, S), fired(S), orientation(0, S), wumpus(X2, Y, S), X2 > X.
wumpus_killed(S) :- at(X, Y, S), fired(S), orientation(1, S), wumpus(X, Y2, S), Y2 > Y.
wumpus_killed(S) :- at(X, Y, S), fired(S), orientation(2, S), wumpus(X2, Y, S), X2 < X.
wumpus_killed(S) :- at(X, Y, S), fired(S), orientation(0, S), wumpus(X, Y2, S), Y2 < Y.


%% Choice
forward_ok(S) :- SP is S - 1, at(X, Y, SP), ok(X, Y, SP).
forward_danger(S) :- SP is S - 1, not(forward_ok(S)), danger(X, Y, SP).
forward(S) :- forward_ok(S).
forward(S) :- forward_danger(S).

%% Tools
adiacent(X1 , Y1, X2, Y2) :- X1 =:= X2, abs(Y1 - Y2) =:= 1.
adiacent(X1 , Y1, X2, Y2) :- Y1 =:= Y2, abs(X1 - X2) =:= 1.
