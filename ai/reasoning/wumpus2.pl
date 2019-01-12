:- dynamic
    at/2,
    i_have_been_at/2,
    i_know_it_is_safe/2,
    i_know_it_is_stentch/2,
    i_know_it_is_breeze/2,
    direction/1,
    safe/2,
    have/1,
    there_may_be_wumpus/2,
    there_may_be_pit/2,
    turned/1.

%% Initial state
wall(0, _) :- !.
wall(_, 0) :- !.
wall(5, _) :- !.
wall(_, 5) :- !.

pit(3, 3) :- !.
pit(3, 1) :- !.
pit(4, 4) :- !.
gold(2, 3) :- !.

init() :-
    assertz(direction(0)),
    assertz(wumpus(1, 3)),
    assertz(at(1, 1)),
    asserta(i_know_it_is_safe(1, 1)),
    assertz(have(arrow)),
    asserta(turned(0)).

action_turn() :-
    direction(D),
    retract(direction(D)),
    DP is (D + 1) mod 4,
    assertz(direction(DP)),
    asserta(turned(DP)).

action_multi_turn(D) :-
    direction(DP),
    retract(direction(DP)),
    assertz(direction(D)),
    asserta(turned(D)).

action_move() :-
    at(X, Y),
    (retractall(turned(_)); !),
    direction(D), asserta(turned(D)),
    retract(at(X, Y)),
    (
        (direction(0), XP is X + 1, asserta(i_have_been_at(XP, Y)), assertz(at(XP, Y)), i_am_aware_of(XP, Y));
        (direction(1), YP is Y + 1, asserta(i_have_been_at(X, YP)), assertz(at(X, YP)), i_am_aware_of(X, YP));
        (direction(2), XP is X - 1, asserta(i_have_been_at(XP, Y)), assertz(at(XP, Y)), i_am_aware_of(XP, Y));
        (direction(3), YP is Y - 1, asserta(i_have_been_at(X, YP)), assertz(at(X, YP)), i_am_aware_of(X, YP))
    ),
    infer_safe_positions().


infer_safe_positions() :-
    (
        (at(X, Y), i_know_it_is_safe(X, Y));
        (
            infer_there_may_be_wumpus(),
            infer_there_may_be_pit()

        )
    ),
    %% I would like it could infer these by himself. I do not know how, though...
    (there_may_be_wumpus(X, Y), there_may_be_pit(X, Y), asserta(i_know_it_is_safe(X, Y))); !.

infer_there_may_be_wumpus() :-
    at(X, Y), i_know_it_is_stentch(X, Y),
    (
        XP is X + 1, \+ wall(XP, Y), asserta(there_may_be_wumpus(XP, Y));
        XP is X - 1, \+ wall(XP, Y), asserta(there_may_be_wumpus(XP, Y));
        YP is Y + 1, \+ wall(X, YP), asserta(there_may_be_wumpus(X, YP));
        YP is Y - 1, \+ wall(X, YP), asserta(there_may_be_wumpus(X, YP))
    ).

infer_there_may_be_pit() :-
    at(X, Y), i_know_it_is_breeze(X, Y),
    (
        XP is X + 1, \+ wall(XP, Y), asserta(there_may_be_pit(XP, Y));
        XP is X - 1, \+ wall(XP, Y), asserta(there_may_be_pit(XP, Y));
        YP is Y + 1, \+ wall(X, YP), asserta(there_may_be_pit(X, YP));
        YP is Y - 1, \+ wall(X, YP), asserta(there_may_be_pit(X, YP))
    ).

i_am_aware_of(X, Y) :-
    (breeze(X, Y), asserta(i_know_it_is_breeze(X, Y)));
    (stentch(X, Y), asserta(i_know_it_is_stentch(X, Y)));
    asserta(i_know_it_is_safe(X, Y)).

breeze(X, Y) :-
    pit(XP, Y), X is XP + 1, !;
    pit(XP, Y), X is XP - 1, !;
    pit(X, YP), Y is YP - 1, !;
    pit(X, YP), Y is YP + 1, !.

stentch(X, Y) :-
    wumpus(XP, Y), X is XP + 1, !;
    wumpus(XP, Y), X is XP - 1, !;
    wumpus(X, YP), Y is YP - 1, !;
    wumpus(X, YP), Y is YP + 1, !.

there_must_be_wumpus(X, Y) :-
    (XP is X + 1, XQ is X - 1, i_know_it_is_stentch(XP, Y), i_know_it_is_stentch(XQ, Y));
    (YP is Y + 1, YQ is Y - 1, i_know_it_is_stentch(X, YP), i_know_it_is_stentch(X, YQ));
    (XP is X + 1, YP is Y + 1, i_know_it_is_stentch(X, YP), i_know_it_is_stentch(XP, Y));
    (XP is X - 1, YP is Y - 1, i_know_it_is_stentch(X, YP), i_know_it_is_stentch(XP, Y));
    (XP is X + 1, YP is Y - 1, i_know_it_is_stentch(X, YP), i_know_it_is_stentch(XP, Y));
    (XP is X - 1, YP is Y + 1, i_know_it_is_stentch(X, YP), i_know_it_is_stentch(XP, Y)).

there_must_be_pit(X, Y) :-
    (XP is X + 1, XQ is X - 1, i_know_it_is_breeze(XP, Y), i_know_it_is_breeze(XQ, Y));
    (YP is Y + 1, YQ is Y - 1, i_know_it_is_breeze(X, YP), i_know_it_is_breeze(X, YQ));
    (XP is X + 1, YP is Y + 1, i_know_it_is_breeze(X, YP), i_know_it_is_breeze(XP, Y));
    (XP is X - 1, YP is Y - 1, i_know_it_is_breeze(X, YP), i_know_it_is_breeze(XP, Y));
    (XP is X + 1, YP is Y - 1, i_know_it_is_breeze(X, YP), i_know_it_is_breeze(XP, Y));
    (XP is X - 1, YP is Y + 1, i_know_it_is_breeze(X, YP), i_know_it_is_breeze(XP, Y)).

there_must_be_deadly_stuff(X, Y) :-
    there_must_be_wumpus(X, Y); there_must_be_pit(X, Y).

i_am_in_front_of_death() :-
    at(X, Y),
    (
        (direction(0), XP is X + 1, there_must_be_deadly_stuff(XP, Y));
        (direction(1), YP is Y + 1, there_must_be_deadly_stuff(X, YP));
        (direction(2), XP is X - 1, there_must_be_deadly_stuff(XP, Y));
        (direction(3), YP is Y - 1, there_must_be_deadly_stuff(X, YP))
    ).

i_am_in_front_of_wall() :-
    at(X, Y),
    (
        (direction(0), XP is X + 1, wall(XP, Y));
        (direction(1), YP is Y + 1, wall(X, YP));
        (direction(2), XP is X - 1, wall(XP, Y));
        (direction(3), YP is Y - 1, wall(X, YP))
    ).

i_am_in_front_of_safe() :-
    at(X, Y),
    (
        (direction(0), XP is X + 1, i_know_it_is_safe(XP, Y));
        (direction(1), YP is Y + 1, i_know_it_is_safe(X, YP));
        (direction(2), XP is X - 1, i_know_it_is_safe(XP, Y));
        (direction(3), YP is Y - 1, i_know_it_is_safe(X, YP))
    ).

i_have_been_at_in_front() :-
    at(X, Y),
    (
        (direction(0), XP is X + 1, i_have_been_at(XP, Y));
        (direction(1), YP is Y + 1, i_have_been_at(X, YP));
        (direction(2), XP is X - 1, i_have_been_at(XP, Y));
        (direction(3), YP is Y - 1, i_have_been_at(X, YP))
    ).


i_am_in_front_of_wumpus() :-
    at(X, Y),
    wumpus(XW, YW),
    (
        (direction(0), Y =:= YW, X < XW);
        (direction(1), X =:= XW, Y < YW);
        (direction(2), Y =:= YW, X > XW);
        (direction(3), X =:= XW, Y > YW)
    ).

action_shoot() :-
    retract(have(arrow)),
    i_am_in_front_of_wumpus(),
    retractall(wumpus(_, _)),
    retractall(i_know_it_is_stentch(_, _)).

win() :-
    at(1, 1),
    have(gold).

lost() :-
    at(X, Y),
    (wumpus(X, Y); pit(X, Y)).

explore() :-
    init(),
    go().

i_have_won() :-
    (writef('0'), win(), writef('I have won\n')).

i_have_lost() :-
    (writef('1'), lost(), writef('I have lost\n')).

i_grab_gold() :-
    (writef('2'), at(X, Y), \+ have(gold), gold(X, Y), assertz(have(gold)), writef('I have grabbed gold\n'), go()).

i_safely_proceed() :-
    (writef('3'), at(X, Y), (i_know_it_is_safe(X, Y); i_am_in_front_of_safe()), \+ i_am_in_front_of_wall(), action_move(), writef('I safely move\n'), go()).

i_kill_the_wumpus() :-
    (writef('4'), have(arrow), i_am_in_front_of_wumpus(), action_shoot(), writef('I shot at the wumpus\n'), go()).

i_turn() :-
    (writef('5'), action_turn(), writef('I turn\n'), go()).

i_unsafely_proceed() :-
    (writef('6'), \+ i_am_in_front_of_death(), action_move(), writef('I unsafely move\n'), go()).

i_have_done_a_complete_turn() :-
    turned(0),
    turned(1),
    turned(2),
    turned(3).


i_return_as_fast_as_possible() :-
    have(gold),
    at(X, Y),
    (
        (X > 1, XP is X - 1, i_know_it_is_safe(XP, Y), action_multi_turn(2));
        (Y > 1, YP is Y - 1, i_know_it_is_safe(X, YP), action_multi_turn(3))
    ),
    action_move(),
    writef('Let\'s return as fast as possible'),
    go().

go() :-
    (
        at(X, Y), direction(D),
        (
            (have(gold), writef('I am at (%w, %w), dir %w, WITH GOLD\n', [X, Y, D]));
            writef('I am at (%w, %w), dir %w, WITHOUT GOLD\n', [X, Y, D])
        )
    ),
    (
        i_have_won();
        i_have_lost();
        i_grab_gold();
        i_return_as_fast_as_possible();
        \+ i_have_been_at_in_front(), i_safely_proceed();
        i_kill_the_wumpus();
        \+ i_have_done_a_complete_turn(), i_turn();
        i_safely_proceed();
        i_turn();
        i_unsafely_proceed()
    ).
