%% Initial state
wall(0, _) :- !.
wall(_, 0) :- !.
wall(5, _) :- !.
wall(_, 5) :- !.
wumpus(1, 3, 0) :- !.
pit(3, 3) :- !.
pit(3, 1) :- !.
pit(4, 4) :- !.
gold(2, 3) :- !.
status(0) :- !.

%% Basic movement rules
direction(1, 1, 0, 0) :- !.
direction(X, Y, O, S) :-
    writef('Direction %w, %w, %w at status %w?\n', [X, Y, O, S]),
    turned(X, Y, SP), !,
    direction(X, Y, OP, SP), !,
    S is SP + 1, O is (OP + 1) mod 3, !,
    writef('--------> Direction %w, %w, %w at status %w\n', [X, Y, O, S]).


at(1, 1, S) :- S =:= 0, !.
at(X, Y, S) :-
    writef('Am I at %w, %w at status %w?\n', [X, Y, S]),
    (
        S \== 0,
        (
            at(XP, Y, SP), forwarded(XP, Y, SP), direction(XP, Y, 0, SP), S is SP + 1, X is XP + 1, X > 0, !;
            at(X, YP, SP), forwarded(X, YP, SP), direction(X, YP, 1, SP), S is SP + 1, Y > 0, Y is YP + 1, !;
            at(XP, Y, SP), forwarded(XP, Y, SP), direction(XP, Y, 2, SP), S is SP + 1, X is XP - 1, !;
            at(X, YP, SP), forwarded(X, YP, SP), direction(X, YP, 3, SP), S is SP + 1, Y is YP - 1, !
        ),
        writef('--------> I am at %w, %w, status %w\n', [X, Y, S])
    );
    (writef('--------> I am NOT at %w, %w, status %w\n', [X, Y, S]), fail).

%% Derived table state
stentch(X, Y, S) :-
    wumpus(XP, Y, S), X is XP + 1, !;
    wumpus(XP, Y, S), X is XP - 1, !;
    wumpus(X, YP, S), Y is YP - 1, !;
    wumpus(X, YP, S), Y is YP + 1, !.

breeze(X, Y) :-
    pit(XP, Y), X is XP + 1, !;
    pit(XP, Y), X is XP - 1, !;
    pit(X, YP), Y is YP - 1, !;
    pit(X, YP), Y is YP + 1, !.


%% Actions classification
dead(0) :- !, fail.
dead(S) :-
    dead(SP), !, S > 0, S is SP + 1, !;
    wumpus(X, Y, S), !, at(X, Y, S), !;
    pit(X, Y), !, at(X, Y, S).

danger(X, Y, S) :-
    stentch(X, Y, S);
    breeze(X, Y).
ok(X, Y, S) :- not(dead(S)), not(danger(X, Y, S)).

hold_gold(0) :- fail.
hold_gold(S) :-
    gold(X, Y), !, at(X, Y, S), !;
    hold_gold(SP), S is SP + 1.
win(S) :- hold_gold(S), X is 1, Y is 1, at(X, Y, S).
wumpus_killed(S) :-
    at(X, Y, S), fired(S), direction(X, Y, 0, S), wumpus(X2, Y, S), X2 > X, !;
    at(X, Y, S), fired(S), direction(X, Y, 1, S), wumpus(X, Y2, S), Y2 > Y, !;
    at(X, Y, S), fired(S), direction(X, Y, 2, S), wumpus(X2, Y, S), X2 < X, !;
    at(X, Y, S), fired(S), direction(X, Y, 3, S), wumpus(X, Y2, S), Y2 < Y.


%% Choice to move
forwarded(X, Y, S) :-
    writef('Forwarded at %w, %w, status %w?\n', [X, Y, S]),
    (
        ok(X, Y, S);
        danger(X, Y, S), !, not(i_am_in_front_of_death(X, Y, S))
    ),
    writef('--------> Forwarded at %w, %w, status %w\n', [X, Y, S]).

turned(X, Y, S) :- writef('Did I turn at status %w?\n', [S]), i_am_in_front_of_death(X, Y, S), writef('--------> I turned at status %w\n', [S]).
i_am_in_front_of_death(X, Y, S) :-
    writef('Am I in front of death at %w, %w, status %w?\n', [X, Y, S]),
    (
        i_am_in_front_of_wumpus(X, Y, S), !;
        i_am_in_front_of_pit(X, Y, S)
    ),
    writef('--------> I am in front of death at %w, %w, status %w=\n', [X, Y, S]).

%% Inference on dangers
fired(S) :-
    at(X, Y, SP), !,
    S > 0, SP is S - 1,
    not(fired(SP)),
    stentch(X, Y, SP),
    not(wumpus_killed(SP)),
    i_am_in_front_of_wumpus(X, Y, SP).

i_am_in_front_of_pit(X, Y, S) :-
    at(X, Y, S), !,
    (
        direction(X, Y, 0, S), !, XP is X + 1, there_must_be_pit(XP, Y, S);
        direction(X, Y, 1, S), !, YP is Y + 1, there_must_be_pit(X, YP, S);
        direction(X, Y, 2, S), !, X > 0, XP is X - 1, there_must_be_pit(XP, Y, S);
        direction(X, Y, 3, S), !, Y > 0, YP is Y - 1, there_must_be_pit(X, YP, S)
    ).

there_must_be_pit(X, Y, S) :-
    XP is X - 1, XQ is X + 1, pit_or_wall(XP, Y, S), pit_or_wall(XQ, Y, S), !;
    XP is X - 1, YQ is Y + 1, pit_or_wall(XP, Y, S), pit_or_wall(X, YQ, S), !;
    XP is X - 1, YP is Y - 1, pit_or_wall(XP, Y, S), pit_or_wall(X, YP, S), !;
    XQ is X + 1, YP is Y - 1, pit_or_wall(XQ, Y, S), pit_or_wall(X, YP, S), !;
    XQ is X + 1, YQ is Y + 1, pit_or_wall(XQ, Y, S), pit_or_wall(X, YQ, S), !;
    YP is Y - 1, YQ is Y + 1, pit_or_wall(X, YP, S), pit_or_wall(X, YQ, S).

i_am_in_front_of_wumpus(X, Y, S) :-
    at(X, Y, S), !, direction(X, Y, 0, S), !, XP is X + 1, there_must_be_wumpus(XP, Y, S);
    at(X, Y, S), !, direction(X, Y, 1, S), !, YP is Y + 1, there_must_be_wumpus(X, YP, S);
    at(X, Y, S), !, direction(X, Y, 2, S), !, X > 0, XP is X - 1, there_must_be_wumpus(XP, Y, S);
    at(X, Y, S), !, direction(X, Y, 3, S), !, Y > 0, YP is Y - 1, there_must_be_wumpus(X, YP, S).

there_must_be_wumpus(X, Y, S) :-
    XP is X - 1, XQ is X + 1, stentch_or_wall(XP, Y, S), stentch_or_wall(XQ, Y, S), !;
    XP is X - 1, YQ is Y + 1, stentch_or_wall(XP, Y, S), stentch_or_wall(X, YQ, S), !;
    XP is X - 1, YP is Y - 1, stentch_or_wall(XP, Y, S), stentch_or_wall(X, YP, S), !;
    XQ is X + 1, YP is Y - 1, stentch_or_wall(XQ, Y, S), stentch_or_wall(X, YP, S), !;
    XQ is X + 1, YQ is Y + 1, stentch_or_wall(XQ, Y, S), stentch_or_wall(X, YQ, S), !;
    YP is Y - 1, YQ is Y + 1, stentch_or_wall(X, YP, S), stentch_or_wall(X, YQ, S).

stentch_or_wall(X, Y, S) :-
    X > 0, Y > 0, wall(X, Y);
    X > 0, Y > 0, stentch(X, Y, S).  %% TODO here I want to have been there at status S.

pit_or_wall(X, Y, S) :-
    X > 0, Y > 0, wall(X, Y);
    X > 0, Y > 0, pit(X, Y, S).
%% Tools
adiacent(X1 , Y1, X2, Y2) :- X1 =:= X2, abs(Y1 - Y2) =:= 1.
adiacent(X1 , Y1, X2, Y2) :- Y1 =:= Y2, abs(X1 - X2) =:= 1.
