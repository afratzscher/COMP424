package student_player;

import java.util.ArrayList;
import java.util.List;
import java.util.*;
import boardgame.Move;

import pentago_twist.PentagoPlayer;
import pentago_twist.PentagoBoardState.Piece;
import pentago_twist.PentagoBoardState;
import pentago_twist.PentagoMove;



public class MyTools {
	public final static int WHITE = 1;
	public final static int BLACK = 2;
	public final static int BLANK = 0;
	private final static int WIN = 0;
	private final static long MASK_WIN_HORIZONTAL = 0b111110000000000000000000000000000000L;
	private final static long MASK_WIN_VERTICAL =0b100000100000100000100000100000000000L;
	private final static long MASK_WIN_DIAG_LR =0b100000010000001000000100000010000000L;
	private final static long MASK_WIN_DIAG_RL =0b1000010000100001000010000000000L;
	private final static long MASK_MIDDLE = 0b000000010010000000000000010010000000L;
	private final static long MASK_WIN_DIAG_LR4 =0b001000000100000010000001000000000000L;
	private final static long MASK_WIN_DIAG_LR3 =0b000100000010000001000000000000000000L;
	private final static long MASK_WIN_DIAG_LR2 =0b000010000001000000000000000000000000L;

	private final static long MASK_WIN_DIAG_RL4 =0b000100001000010000100000000000000000L;
	private final static long MASK_WIN_DIAG_RL3 =0b001000010000100000000000000000000000L;
	private final static long MASK_WIN_DIAG_RL2 =0b010000100000000000000000000000000000L;
	private final static int BOARD_SIZE = 6;
	private final static int INFINITY = 1000000000;
	private static int bestvalue;
	private static int value;

	// represents board as a long int
	// for binary, 0 = empty, 1 = occupied (by white in whiteboard, by black in blackboard)
	// converts binary to long int -> e.g. 1001 in binary = 9 in int
	public static long[] getBitBoard(PentagoBoardState boardState)
	{
		long whiteBoard = 0;
		long blackBoard = 0;
		for (int i = 0; i < 6; i++)
		{
			for (int j = 0; j < 6; j++)
			{
				Piece p = boardState.getPieceAt(i,j);
				if (p == Piece.BLACK)
				{
					blackBoard = (blackBoard | (((long) 1) << (35-(6*i+j))));
				}
				else if (p == Piece.WHITE)
				{
					whiteBoard = (whiteBoard | (((long) 1) << (35-(6*i+j))));
				}
			}
		}       
		return new long[] {blackBoard, whiteBoard};
	}

	public static long allLegalMoves(long myBoard, long yourBoard) {
		long mask = 0b111111111111111111111111111111111111L;
		return (myBoard | yourBoard) ^ mask;
	}

	public static long[] makeMove(long myBoard, long yourBoard, boolean myturn, long move)
	{
		return new long[] {myBoard | move, yourBoard};

	}
	// negamax with alpha beta pruning
	public static int negamax(int depth, int alpha ,int beta, long endtime, long myBoard, long yourBoard, boolean myturn) 
	{

		//check game over;
		if (depth == 0) 
		{
			return evaluate(myBoard, yourBoard);
		}

		bestvalue = -INFINITY;

		long moves = allLegalMoves(myBoard, yourBoard);

		for(int i=0;i<36;i++) // go through all moves
		{
			// if run out of time, return best value so far
			if (System.currentTimeMillis() > endtime)
			{
				return bestvalue;
			}

			long theMove = (moves & ((long) 1 << (i)));

			if ((theMove >>> i) == 1) // if possible move
			{
				long tmpMy = myBoard;
				long tmpYour = yourBoard;
				long[] tmp = makeMove(myBoard, yourBoard, myturn, theMove);
				myBoard = tmp[0];
				yourBoard = tmp[1];
				value = -negamax(depth-1, -beta, -alpha, endtime, myBoard, yourBoard, !myturn);

				bestvalue = Math.max(value, bestvalue);
				if (bestvalue >= beta) { return beta; }
				if (value > alpha) { alpha = bestvalue; } 

				myBoard = tmpMy;
				yourBoard = tmpYour;
			}
		}
		return bestvalue;    	
	}


	//evaluation function
	public static int evaluate(long myBoard, long yourBoard)
	{
		long maskh = MASK_WIN_HORIZONTAL;
		long maskv = MASK_WIN_VERTICAL;
		long masklr = MASK_WIN_DIAG_LR;
		long maskrl = MASK_WIN_DIAG_RL;
		long masklr4 = MASK_WIN_DIAG_LR4;
		long masklr3 = MASK_WIN_DIAG_LR3;
		long masklr2 = MASK_WIN_DIAG_LR2;
		long maskrl4 = MASK_WIN_DIAG_RL4;
		long maskrl3 = MASK_WIN_DIAG_RL3;
		long maskrl2 = MASK_WIN_DIAG_RL2;
		int cumscore = 0;

		//check horizontal and vertical
		for (int i = 0; i < 6; i++)
		{
			// for horizontal
			cumscore += scoreBoth(myBoard, yourBoard, maskh);
			cumscore += scoreBoth(myBoard, yourBoard, maskh >>> 1); // goes from 111110 to 011111 
			maskh = maskh >>> 6; // goes to next row

			// for vertical
			cumscore += scoreBoth(myBoard, yourBoard, maskv);
			cumscore += scoreBoth(myBoard, yourBoard, maskv >>> 6); 
			maskh = maskv >>> 1; // goes to next column
		}

		// for diagonals
		// L to R diagonal first
		// for 5 in a row
		cumscore += scoreBoth(myBoard, yourBoard, masklr);
		masklr = masklr >>> 1; // shifts 1 bit to RIGHT
		cumscore += scoreBoth(myBoard, yourBoard, masklr);
		masklr = masklr >>> 5; // first 1 goes to next row
		cumscore += scoreBoth(myBoard, yourBoard, masklr);
		masklr = masklr >>> 1; // shifts 1 bit
		cumscore += scoreBoth(myBoard, yourBoard, masklr);
		//for 4 in a row
		cumscore += scoreBoth(myBoard, yourBoard, masklr4);
		masklr4 = masklr4 >>>10;
		cumscore += scoreBoth(myBoard, yourBoard, masklr4);
		//for 3 in a row
		cumscore += scoreBoth(myBoard, yourBoard, masklr3);
		masklr3 = masklr3 >>>15;
		cumscore += scoreBoth(myBoard, yourBoard, masklr3);
		//for 2 in a row
		cumscore += scoreBoth(myBoard, yourBoard, masklr2);
		masklr2 = masklr2 >>>20;
		cumscore += scoreBoth(myBoard, yourBoard, masklr2);


		// then R to L diagonal
		cumscore += scoreBoth(myBoard, yourBoard, maskrl);
		maskrl = maskrl << 1; // shifts 1 bit to LEFT
		cumscore += scoreBoth(myBoard, yourBoard, maskrl);
		maskrl = maskrl >>> 7; 
		cumscore += scoreBoth(myBoard, yourBoard, maskrl);
		maskrl = maskrl >>> 1; // shifts 1 bit
		cumscore += scoreBoth(myBoard, yourBoard, maskrl);
		//for 4 in a row
		cumscore += scoreBoth(myBoard, yourBoard, maskrl4);
		maskrl4 = maskrl4 >>>14;
		cumscore += scoreBoth(myBoard, yourBoard, maskrl4);
		//for 3 in a row
		cumscore += scoreBoth(myBoard, yourBoard, maskrl3);
		maskrl3 = maskrl3 >>>21;
		cumscore += scoreBoth(myBoard, yourBoard, maskrl3);
		//for 2 in a row
		cumscore += scoreBoth(myBoard, yourBoard, maskrl2);
		maskrl2 = maskrl2 >>>28;
		cumscore += scoreBoth(myBoard, yourBoard, maskrl2);

		return cumscore;
	}

	// helper function -> counts score for both my and other board (because want best for you and worst for opponent)
	public static int scoreBoth(long myBoard, long yourBoard, long mask)
	{
		return score(myBoard, yourBoard, mask) - score(yourBoard, myBoard, mask);
		//if opponent score very high, get low score -> because want to both have you do well and opponent do poorly
	}

	// helper function -> gets occurence of 5 in row, 4 in row, 3 in row, marbles in center
	public static int score(long board, long bBoard, long mask)
	{
		if ((bBoard&mask)!=0) return 0;
		long score=board&mask;
		long middle = board&MASK_MIDDLE;
		int middlecnt = Long.bitCount(middle);
		int result=Long.bitCount(score); // gets number of 1s for board
		if (result==0) return 0; // if no 1s, return 0
		if (result == 5) return INFINITY; // if win, return infinity

		if (middlecnt != 0) // patterns involving middle marbles have more worth
		{
			if (result==1) return middlecnt * 5;
			else if (result==2) return middlecnt*10;
			else if (result==3) return middlecnt*100;
			else if (result==4) return middlecnt*1000;
		}
		else
		{
			if (result==1) return  5;
			else if (result==2) return 10;
			else if (result==3) return 100;
			else if (result==4) return 1000;
		}
		return 0; // if no, return 0

	}

}