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
status(S) :- S > 0, SP is S - 1, result(a, SP).

%% Basic movement rules
orientation(O, S) :- S > 0, SP is S - 1, OP is (O - 1) mod 3, status(SP), orientation(OP, SP), turned(SP).
at(X, Y, S) :- S > 0, SP is S - 1, forwarded(SP), X > 0, XP is X - 1, at(XP, Y, SP), orientation(0, SP).
at(X, Y, S) :- S > 0, SP is S - 1, forwarded(SP), Y > 0, YP is Y - 1, at(X, YP, SP), orientation(1, SP).
at(X, Y, S) :- S > 0, SP is S - 1, forwarded(SP), XP is X + 1, at(XP, Y, SP), orientation(2, SP).
at(X, Y, S) :- S > 0, SP is S - 1, forwarded(SP), YP is Y + 1, at(X, YP, SP), orientation(3, SP).

%% Derived table state
stentch(X, Y, S) :- X > 0, XP is X - 1, wumpus(XP, Y, S).
stentch(X, Y, S) :- XP is X + 1, wumpus(XP, Y, S).
stentch(X, Y, S) :- YP is Y + 1, wumpus(X, YP, S).
stentch(X, Y, S) :- Y > 0, YP is Y - 1, wumpus(X, YP, S).
breeze(X, Y) :- X > 0, XP is X - 1, pit(XP, Y).
breeze(X, Y) :- XP is X + 1, pit(XP, Y).
breeze(X, Y) :- YP is Y + 1, pit(X, YP).
breeze(X, Y) :- Y > 0, YP is Y - 1, pit(X, YP).


%% Actions classification
dead(X, Y, S) :- at(X, Y, S), wumpus(X, Y, S).
dead(X, Y, S) :- at(X, Y, S), pit(X, Y).
danger(X, Y, S) :- at(X, Y, S), stentch(X, Y, S).
danger(X, Y, S) :- at(X, Y, S), breeze(X, Y).
ok(X, Y, S) :- not(dead(X, Y, S)), not(danger(X, Y, S)).
hold_gold(S) :- S > 0, SP is S - 1, hold_gold(SP).
hold_gold(S) :- at(X, Y, S), gold(X, Y).
win(S) :- hold_gold(S), at(1, 1, S).
wumpus(X, Y, S) :- S > 0, SP is S - 1, wumpus(X, Y, SP), not(wumpus_killed(S)).
wumpus_killed(S) :- at(X, Y, S), fired(S), orientation(0, S), wumpus(X2, Y, S), X2 > X.
wumpus_killed(S) :- at(X, Y, S), fired(S), orientation(1, S), wumpus(X, Y2, S), Y2 > Y.
wumpus_killed(S) :- at(X, Y, S), fired(S), orientation(2, S), wumpus(X2, Y, S), X2 < X.
wumpus_killed(S) :- at(X, Y, S), fired(S), orientation(0, S), wumpus(X, Y2, S), Y2 < Y.


%% Choice to move
forward_ok(S) :- S > 0, SP is S - 1, at(X, Y, SP), ok(X, Y, SP).
forward_danger(S) :- S > 0, SP is S - 1, not(forward_ok(S)), danger(X, Y, SP).
forwarded(S) :- forward_ok(S).
forwarded(S) :- forward_danger(S).

%% Fire
fired(S) :- S > 0, SP is S - 1, not(fired(SP)), stentch(X, Y, SP), at(X, Y, SP), i_am_in_front_of_wumpus(X, Y, SP).
i_am_in_front_of_wumpus(X, Y, S) :- orientation(0, S), at(X, Y, S), XP is X + 1, there_must_be_wumpus(XP, Y, S).
i_am_in_front_of_wumpus(X, Y, S) :- orientation(1, S), at(X, Y, S), YP is Y + 1, there_must_be_wumpus(X, YP, S).
i_am_in_front_of_wumpus(X, Y, S) :- orientation(2, S), at(X, Y, S), X > 0, XP is X - 1, there_must_be_wumpus(XP, Y, S).
i_am_in_front_of_wumpus(X, Y, S) :- orientation(3, S), at(X, Y, S), Y > 0, YP is Y - 1, there_must_be_wumpus(X, YP, S).
there_must_be_wumpus(X, Y, S) :- XP is X - 1, XQ is X + 1, YP is Y - 1, YQ is Y + 1, stentch_or_wall(XP, Y, S), stentch_or_wall(XQ, Y, S), stentch_or_wall(X, YP, S), stentch_or_wall(X, YQ, S).
stentch_or_wall(X, Y, S) :- X > 0, Y > 0, wall(X, Y).
stentch_or_wall(X, Y, S) :- X > 0, Y > 0, stentch(X, Y, S).

%% Tools
adiacent(X1 , Y1, X2, Y2) :- X1 =:= X2, abs(Y1 - Y2) =:= 1.
adiacent(X1 , Y1, X2, Y2) :- Y1 =:= Y2, abs(X1 - X2) =:= 1.
