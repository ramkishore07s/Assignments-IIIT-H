pragma solidity ^0.5.11;

contract XO {
    
    uint8[3][3] grid;
    bool gameover;
    
    uint8 p1wins;
    uint8 p2wins;
    uint8 draws;
    
    uint8 gameno;
    uint8 moves;
    
    address payable owner; 
    address payable player1;
    address payable player2;
    address null_;
    
    bool started;
    uint bet;
    uint balance;
    
    uint8 maxgames;
    
    modifier onlyCreator() {
        require(msg.sender == owner);
        _;
    }    
    
    modifier onlyPlayer() {
        require(!(msg.sender == owner));
        _;
    }
    
    constructor() payable public {
        gameover = false;
        gameno = 0;
        owner = msg.sender;
        started = false;
        moves = 0;
        balance = uint(msg.value);
        maxgames = 4;
    }
    
    function register(bool _randomplayer) payable public returns (bool) {
        require(!(msg.sender == owner), 'owner cannot play');
        require((msg.value > 0) || _randomplayer, 'place a bet');
        require(!started, 'game has started');
        require(!(msg.sender == player1), 'you are already a player');    
        
        if (player1 == address(0)) {
            player1 = msg.sender;
            bet = uint(msg.value);
            
            if (_randomplayer) {
                require(msg.value == 0, 'cannot bet against random player');
                player2 = owner;
                bet = 0;
                started = true;
            }
            init();
            return true;
        }
        else {
            if (player2 == address(0)) {
                // require(msg.value == bet, "not correct bet value");
                player2 = msg.sender;
                started = true;
                
                if (bet > msg.value) { player1.transfer(bet - msg.value); bet = msg.value; }
                if (bet < msg.value) { player2.transfer(msg.value - bet); }
                init();
                return true;
            }
        }
        return false;
    }
    
    function get_bet() public view returns (uint) {
        return bet;
    }
    
    function get_states() public view returns (uint8[3][3] memory) {
        return grid;
    }
    
    function get_turn() public view returns (uint) {
        if ((gameno + moves) % 2 == 0)
            return 1;
        return 2;
    }
    
    function randommove() public {
        uint8 move = random() + 1;
        uint8 j = 0;
        for (uint8 i=0; i<=8; i++) {
            if (grid[i/3][i%3] == 0) { j = j + 1; }
            if (j == move) { grid[i/3][i%3] = 2; moves = moves + 1; return;}
        }
    }
    
    function play(uint8 x, uint8 y) public returns (uint8[3][3] memory) {
        require(started, 'game not started');
        require(gameno < maxgames, 'game over');
        require(grid[x][y] == uint8(0), 'invalid move');
        
        uint8 marker;
        
        if ((gameno + moves) % 2 == 0) { require(msg.sender == player1, 'player1 turn'); marker = 1;}
        else {require(msg.sender == player2, 'player2 turn'); marker = 2;}
        
        grid[x][y] = marker;
        moves = moves + 1;
        
        uint8 winner = check();
        
        if ((player2 == owner) && (winner == 0)) {
            randommove();
            winner = check();
        }
        
        if (!(winner == 0)) {
            gameno = gameno + 1;
            init();
            moves = 0;
            if (winner == 1) { p1wins = p1wins + 1; }
            else { p2wins = p2wins + 1; }
        }
        
        if (moves == 8) {
            moves = 0;
            gameno = gameno + 1;
            init();
            draws = draws + 1;
        }
        
        if (p1wins + p2wins + draws == maxgames) {
            sendPrize();
        }
        
        return grid;
    }
    
    function isEqualThree(uint8 x, uint8 y, uint8 z) private pure returns(bool) {
        if ((x == y) && (y == z)) { return true; }
        return false;
    }
    
    function sendPrize() private {
        if (p1wins > p2wins) { player1.transfer(2 * bet); }
        if (p2wins > p1wins) { player2.transfer(2 * bet); }
        if (p1wins == p2wins) { owner.transfer(2 * bet); }
    }

    function check() private view returns (uint8) {
        // check rows
        for (uint i=0; i<3; i++) {
            if (isEqualThree(grid[i][0], grid[i][1], grid[i][2])) {
                if (grid[i][0] != 0)
                    return grid[i][0];
            }
        }
        
        // check columns
        for (uint i=0; i<3; i++) {
            if (isEqualThree(grid[0][i], grid[1][i], grid[2][i])) {
                if (grid[0][i] != 0)
                    return grid[0][i];
            }
        }
        
        // check diagonals
        if (isEqualThree(grid[1][1], grid[2][2], grid[0][0])) {
            if (grid[1][1] != 0)
                return grid[1][1];
        }
        
        if (isEqualThree(grid[2][0], grid[0][2], grid[1][1])) {
            if (grid[2][0] != 0)
                return grid[1][1];
        }
        return 0;
    }
    
    function init() private {
        for (uint i=0; i<3; i++)
            for (uint j=0; j<3; j++)
                grid[i][j] = 0;
        if ((gameno < maxgames) && ((gameno % 2 == 1)) && (player2 == owner)) { randommove();}
    }
    
    function test() public returns (uint8) {
        play(0, 2);
        play(1, 1);
        play(2, 2);
        play(0, 1);
        play(0, 0);
        play(2, 1);
        return check();
    }
    
    function getStats() public view returns (uint8[3] memory) {
        uint8[3] memory stats;
        stats[0] = p1wins;
        stats[1] = p2wins;
        stats[2] = draws;
        
        return stats;
    }
    
    function random() private view returns (uint8) {
        return uint8(uint256(keccak256(abi.encodePacked(block.timestamp, block.difficulty)))%(7-moves));
    }
}
