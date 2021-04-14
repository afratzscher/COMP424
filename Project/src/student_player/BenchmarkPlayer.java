package student_player;

import boardgame.Move;

import pentago_twist.PentagoMove;
import pentago_twist.PentagoPlayer;
import pentago_twist.PentagoBoardState;


public class BenchmarkPlayer extends PentagoPlayer {


    public BenchmarkPlayer() {
        super("Random Non-Stupid Benchmark");
    }


    public Move chooseMove(PentagoBoardState boardState) {

        PentagoMove bestMove = null;
        int bestMoveVal = Integer.MIN_VALUE;
        PentagoBoardState tempBoard;
        for (PentagoMove move : boardState.getAllLegalMoves()) {
            // Clone the board
            tempBoard = (PentagoBoardState) boardState.clone();

            // Process the move
            tempBoard.processMove(move);

            int valueOfNode = BenchmarkTools.minimax(boardState.getTurnPlayer(), tempBoard, 1, false, Integer.MIN_VALUE, Integer.MAX_VALUE);

            if (valueOfNode > bestMoveVal) {
                bestMoveVal = valueOfNode;
                bestMove = move;
            }
        }



        if (bestMove == null) {
            bestMove = (PentagoMove) boardState.getRandomMove();
        }

        return bestMove;
    }
}