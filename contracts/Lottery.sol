// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Lottery {
    address public manager;
    struct Player {
        address payable addr;
        string name;
    }
    Player[] public players;
    Player public winner; // State variable to store the winner's details

    constructor() {
        manager = msg.sender;
    }

    function enter(string memory _name) public payable {
        require(msg.value == 1 ether, "Must send exactly 1 ETH");
        require(players.length < 3, "Lottery is full");

        players.push(Player(payable(msg.sender), _name));
    }

    function pickWinner() public restricted {
        require(players.length == 3, "Not enough players");

        uint index = random() % players.length;
        winner = players[index]; // Store the winner's details
        winner.addr.transfer(address(this).balance);

        // Reset players array
        delete players;
    }

    function random() private view returns (uint) {
        uint256 seed = uint256(keccak256(abi.encodePacked(block.timestamp, block.number)));
        uint256 result = 0;
        for (uint i = 0; i < players.length; i++) {
            result ^= uint256(keccak256(abi.encodePacked(seed, players[i].addr)));
        }
        return result;
    }

    modifier restricted() {
        require(msg.sender == manager, "Only manager can call this function");
        _;
    }

    function getPlayers() public view returns (Player[] memory) {
        return players;
    }

    // New function to get the winner's details
    function getWinner() public view returns (address, string memory) {
        return (winner.addr, winner.name);
    }
}