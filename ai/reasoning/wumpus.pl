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

%% wumpus_log(_).
%% wumpus_log(_, _).
wumpus_log(X) :- writef(X).
wumpus_log(X, Y) :- writef(X, Y).

%% Initial state
wall(0, _) :- !.
wall(_, 0) :- !.
wall(5, _) :- !.
wall(_, 5) :- !.

pit(3, 1) :- !.
pit(4, 4) :- !.
gold(2, 3) :- !.

init(_) :-
    assertz(direction(0)),
    assertz(wumpus(1, 3)),
    assertz(at(1, 1)),
    asserta(i_know_it_is_safe(1, 1)),
    assertz(have(arrow)),
    asserta(turned(0)),
    infer_safe_positions_if_i_am_in_a_clear_position(1, 1).

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

infer_safe_positions_if_i_am_in_a_clear_position(X, Y) :-
    stentch(X, Y); breeze(X, Y);
    (
        (X =:= 5; (XP is X + 1, asserta(i_know_it_is_safe(XP, Y)))),
        (Y =:= 5; (YQ is Y + 1, asserta(i_know_it_is_safe(X, YQ)))),
        (X =:= 1; (XP is X - 1, asserta(i_know_it_is_safe(XP, Y))));
        (Y =:= 1; (YQ is Y - 1, asserta(i_know_it_is_safe(X, YQ))))
    ).

action_move(_) :-
    at(X, Y),
    (retractall(turned(_)); !),
    direction(D), asserta(turned(D)),
    retract(at(X, Y)),
    (
        (direction(0), XP is X + 1, asserta(i_have_been_at(XP, Y)), assertz(at(XP, Y)), i_am_aware_of(XP, Y));
        (direction(1), YQ is Y + 1, asserta(i_have_been_at(X, YQ)), assertz(at(X, YQ)), i_am_aware_of(X, YQ));
        (direction(2), XP is X - 1, asserta(i_have_been_at(XP, Y)), assertz(at(XP, Y)), i_am_aware_of(XP, Y));
        (direction(3), YQ is Y - 1, asserta(i_have_been_at(X, YQ)), assertz(at(X, YQ)), i_am_aware_of(X, YQ))
    ),
    infer_safe_positions_if_i_am_in_a_clear_position(X, Y),
    infer_safe_positions().


infer_safe_positions() :-
    infer_there_may_be_wumpus(),
    infer_there_may_be_pit(),
    %% I would like it could infer these by himself. I do not know how, though...
    infer_safe().


infer_safe() :-
    at(X, Y),
    (
    (
        (X =:= 5; (XP is X + 1, there_may_be_wumpus(XP, Y), there_may_be_pit(XP, Y), asserta(i_know_it_is_safe(XP, Y)))),
        (X =:= 1; (XQ is X - 1, there_may_be_wumpus(XQ, Y), there_may_be_pit(XQ, Y), asserta(i_know_it_is_safe(XQ, Y)))),
        (Y =:= 5; (YP is Y + 1, there_may_be_wumpus(X, YP), there_may_be_pit(X, YP), asserta(i_know_it_is_safe(X, YP)))),
        (Y =:= 1; (YQ is Y - 1, there_may_be_wumpus(X, YQ), there_may_be_pit(X, YQ), asserta(i_know_it_is_safe(X, YQ))))
    ); true
    ).


infer_there_may_be_wumpus() :-
    at(X, Y),
    (
    \+ i_know_it_is_stentch(X, Y);
    (
        (X =:= 5; (XP is X + 1, \+ wall(XP, Y), asserta(there_may_be_wumpus(XP, Y)))),
        (X =:= 1; (XQ is X - 1, \+ wall(XQ, Y), asserta(there_may_be_wumpus(XQ, Y)))),
        (Y =:= 5; (YP is Y + 1, \+ wall(X, YP), asserta(there_may_be_wumpus(X, YP)))),
        (Y =:= 1; (YQ is Y - 1, \+ wall(X, YQ), asserta(there_may_be_wumpus(X, YQ))))
    )
    ); true.

infer_there_may_be_pit() :-
    at(X, Y),
    (
    \+ i_know_it_is_breeze(X, Y);
    (
        (X =:= 5; (XP is X + 1, \+ wall(XP, Y), asserta(there_may_be_pit(XP, Y)))),
        (X =:= 1; (XQ is X - 1, \+ wall(XQ, Y), asserta(there_may_be_pit(XQ, Y)))),
        (Y =:= 5; (YP is Y + 1, \+ wall(X, YP), asserta(there_may_be_pit(X, YP)))),
        (Y =:= 1; (YQ is Y - 1, \+ wall(X, YQ), asserta(there_may_be_pit(X, YQ))))
    )
    ); true.

i_am_aware_of(X, Y) :-
    (breeze(X, Y), asserta(i_know_it_is_breeze(X, Y)));
    (stentch(X, Y), asserta(i_know_it_is_stentch(X, Y)));
    wumpus(X, Y); pit(X, Y); wumpus_log('dino %w, %w\n', [X, Y]), asserta(i_know_it_is_safe(X, Y)).

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

i_am_in_front_of_wall(_) :-
    at(X, Y),
    (
        (direction(0), XP is X + 1, wall(XP, Y));
        (direction(1), YP is Y + 1, wall(X, YP));
        (direction(2), XP is X - 1, wall(XP, Y));
        (direction(3), YP is Y - 1, wall(X, YP))
    ).

i_am_in_front_of_safe(_) :-
    at(X, Y),
    (
        (direction(0), XP is X + 1, i_know_it_is_safe(XP, Y));
        (direction(1), YP is Y + 1, i_know_it_is_safe(X, YP));
        (direction(2), XP is X - 1, i_know_it_is_safe(XP, Y));
        (direction(3), YP is Y - 1, i_know_it_is_safe(X, YP))
    ).

i_have_been_at_in_front(_) :-
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

win(_) :-
    at(1, 1),
    have(gold).

lost(_) :-
    at(X, Y),
    (wumpus(X, Y); pit(X, Y)).

explore(RESULT) :-
    init(_),
    go([], RESULT).


define_and_fail(CURRENT_STATUS, RESULT) :-
    append(CURRENT_STATUS, [], RESULT), false.

append_with_status(CURRENT_STATUS, V, RESULT) :-
    at(X, Y), direction(D),
    format(atom(VALUE), '[~w] at (~w, ~w, dir ~w)', [V, X, Y, D]),
    append(CURRENT_STATUS, [VALUE], RESULT).

i_have_won(CURRENT_STATUS, RESULT) :-
    (
        wumpus_log('0'),
        (
            (win(_), append_with_status(CURRENT_STATUS, 'WIN', RESULT));
            define_and_fail(CURRENT_STATUS, result)
        ),
        wumpus_log('I have won\n')
    ).

i_have_lost(CURRENT_STATUS, RESULT) :-
    (
        wumpus_log('1'),
        (
            (lost(_), append_with_status(CURRENT_STATUS, 'LOSE', RESULT));
            define_and_fail(CURRENT_STATUS, RESULT)
        ),
        wumpus_log('I have lost\n')
    ).

i_grab_gold(CURRENT_STATUS, RESULT) :-
    (
        wumpus_log('2'),
        (
            (
                at(X, Y),
                \+ have(gold),
                gold(X, Y),
                assertz(have(gold)),
                append_with_status(CURRENT_STATUS, 'GRAB_GOLD', RESULT1)
            );
            define_and_fail(CURRENT_STATUS, RESULT)
        ),
        wumpus_log('I have grabbed gold\n'),
        go(RESULT1, RESULT)
    ).

i_safely_proceed(CURRENT_STATUS, RESULT) :-
    (
        wumpus_log('3'),
        (
            (
                i_am_in_front_of_safe(_),
                \+ i_am_in_front_of_wall(_),
                action_move(_),
                append_with_status(CURRENT_STATUS, 'MOVE1', RESULT1)
            );
            define_and_fail(CURRENT_STATUS, RESULT)
        ),
        wumpus_log('I safely move\n'),
        go(RESULT1, RESULT)
    ).

i_kill_the_wumpus(CURRENT_STATUS, RESULT) :-
    (
        wumpus_log('4'),
        (
            (
                have(arrow),
                i_am_in_front_of_wumpus(),
                action_shoot(),
                append_with_status(CURRENT_STATUS, 'SHOOT', RESULT1)
            );
            define_and_fail(CURRENT_STATUS, RESULT)
        ),
        wumpus_log('I shot at the wumpus\n'), go(RESULT1, RESULT)
    ).

i_turn(CURRENT_STATUS, RESULT) :-
    (
        wumpus_log('5'),
        (
            (
                action_turn(),
                append_with_status(CURRENT_STATUS, 'TURN', RESULT1)
            );
            define_and_fail(CURRENT_STATUS, RESULT)
        ),
        wumpus_log('I turn\n'),
        go(RESULT1, RESULT)
    ).

i_unsafely_proceed(CURRENT_STATUS, RESULT) :-
    (
        wumpus_log('6'),
        (
            (
                \+ i_am_in_front_of_death(),
                action_move(_),
                append_with_status(CURRENT_STATUS, 'WIN', RESULT1)
            );
            define_and_fail(CURRENT_STATUS, RESULT)
        ),
        wumpus_log('I unsafely move\n'), go(RESULT1, RESULT)
    ).

i_have_done_a_complete_turn(_) :-
    turned(0),
    turned(1),
    turned(2),
    turned(3).


i_return_as_fast_as_possible(CURRENT_STATUS, RESULT) :-
    (
        (
            have(gold),
            at(X, Y),
            (
                (X > 1, XP is X - 1, i_know_it_is_safe(XP, Y), action_multi_turn(2));
                (Y > 1, YP is Y - 1, i_know_it_is_safe(X, YP), action_multi_turn(3))
            ),
            action_move(_),
            append_with_status(CURRENT_STATUS, 'MOVE_BACK', RESULT1)
        );
        define_and_fail(CURRENT_STATUS, RESULT)
    ),
    wumpus_log('Let\'s return as fast as possible'),
    go(RESULT1, RESULT).

go(CURRENT_STATUS, RESULT) :-
    (
        at(X, Y), direction(D),
        (
            (have(gold), wumpus_log('I am at (%w, %w), dir %w, WITH GOLD\n', [X, Y, D]));
            wumpus_log('I am at (%w, %w), dir %w, WITHOUT GOLD\n', [X, Y, D])
        )
    ),
    (
        i_have_won(CURRENT_STATUS, RESULT), !;
        i_have_lost(CURRENT_STATUS, RESULT), !;
        i_grab_gold(CURRENT_STATUS, RESULT);
        i_return_as_fast_as_possible(CURRENT_STATUS, RESULT);
        \+ i_have_been_at_in_front(_), i_safely_proceed(CURRENT_STATUS, RESULT);
        \+ i_have_done_a_complete_turn(_), i_turn(CURRENT_STATUS, RESULT);
        i_safely_proceed(CURRENT_STATUS, RESULT);
        i_turn(CURRENT_STATUS, RESULT);
        i_kill_the_wumpus(CURRENT_STATUS, RESULT);
        i_unsafely_proceed(CURRENT_STATUS, RESULT)
    ).
