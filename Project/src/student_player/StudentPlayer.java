package student_player;

import java.util.ArrayList;
import java.util.List;

import boardgame.Move;

import pentago_twist.PentagoPlayer;
import pentago_twist.PentagoBoardState;
import pentago_twist.PentagoBoardState.Piece;
import pentago_twist.PentagoMove;
/** A player file submitted by a student. */
public class StudentPlayer extends PentagoPlayer {

	/**
	 * You must modify this constructor to return your student number. This is
	 * important, because this is what the code that runs the competition uses to
	 * associate you with your agent. The constructor should do nothing else.
	 */
	public StudentPlayer() {
		super("260705446");
	}

	/**
	 * This is the primary method that you need to implement. The ``boardState``
	 * object contains the current state of the game, which your agent must use to
	 * make decisions.
	 */
	public int maxScore=0;
	public int score;
	public int idx = 0;
	public static int WHITE = 0;
	public static int BLACK = 1;
	public static int BLANK = 2;
	public static int BOARD_SIZE = 6;
	private static final int INFINITY = 1000000000;
	private static int numMoves = 0;

	public int getOpponent(PentagoBoardState temp) { return (temp.getTurnPlayer() == WHITE) ? BLACK : WHITE; }

	public int bestMove(PentagoBoardState temp, long start_time, long end_time)
	{
		maxScore=0;
		idx = 0;
		int bestScore = 0; 

		// get colour I am playing -> 0 = white, 1 = black
		int colour = temp.getTurnPlayer();

		if(getOpponent(temp)==1)
			maxScore = -INFINITY;
		if(getOpponent(temp)==0)
			maxScore = INFINITY;
		if(getOpponent(temp)==1)
			bestScore = -INFINITY;
		if(getOpponent(temp)==0)
			bestScore = INFINITY;

		// have copy of moves
		ArrayList<PentagoMove> moves_copy = temp.getAllLegalMoves();

		PentagoBoardState temp2 = (PentagoBoardState) temp.clone();

		maxScore = 0;
		idx = 0;

		// go through all moves
		for (int i = 0; i < moves_copy.size(); i++)
		{
			long current_time = System.currentTimeMillis();
			// if >endtime (1900 ms), return best so far
			if (current_time > end_time)
			{
				System.out.println("Exceeded time limit");
				return idx;
			}

			// reset board
			temp2 = (PentagoBoardState) temp.clone();
			PentagoMove temp_move = moves_copy.get(i); // get move at index i

			// add move
			temp2.processMove(temp_move); // puts move on board -> get exception if invalid move

			// get board in bitboard (depends on colour)
			long[] boards = MyTools.getBitBoard(temp2);
			long myBoard; long yourBoard;

			if (colour == 0)
			{
				myBoard = boards[1];
				yourBoard = boards[0];
			}
			else
			{
				myBoard = boards[0];
				yourBoard = boards[1];
			}
			int depth = 5; // depth of 5 used
			boolean myTurn = true;

			// get score from move using negamax search (instead of alpha-beta search)
			score = MyTools.negamax(depth, -INFINITY, INFINITY, end_time, myBoard, yourBoard, myTurn);

			//update index if better score
			if(getOpponent(temp)==1)
			{
				if(score>maxScore)
				{
					maxScore=score;
					idx = i;
				}
			}
			if(getOpponent(temp)==0)
			{
				if(score<maxScore)
				{
					maxScore = score;
					idx = i;
				}
			}
		}
		return idx;
	}

	public Move chooseMove(PentagoBoardState boardState) {
		// You probably will make separate functions in MyTools.
		// For example, maybe you'll need to load some pre-processed best opening
		// strategies...

		ArrayList<PentagoMove> moves = boardState.getAllLegalMoves();

		// default first move is middle of first quadrant if possible
		if (boardState.firstPlayer() == 0 && numMoves == 0 && boardState.getTurnPlayer() == 0)
		{
			numMoves += 1;
			return moves.get(7);
		}

		numMoves += 1;
		PentagoBoardState temp =(PentagoBoardState) boardState.clone();
		long starttime = System.currentTimeMillis();
		long endtime = starttime + 1900;
		int bestChoice;
		bestChoice = bestMove(temp,starttime,endtime); //gets best choice
		Move myMove = moves.get(bestChoice);
		//        Move myMove = boardState.getRandomMove();
		return myMove;
	}
}