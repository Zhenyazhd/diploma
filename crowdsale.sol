pragma solidity >= 0.6.0; 


contract Crowdsale {
    
    uint public _totalSupply = 100000000000000000;
    address payable private _wallet = 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
    uint256 private _rate = 1;
    uint256 public _weiRaised;
    address private _owner = 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
    uint private _min = 0;
   
    mapping (address => uint256) private _balances; 
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event SetMin(uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    event TokensPurchased(address indexed purchaser, address indexed beneficiary, uint256 value, uint256 amount);
   
    constructor() {
        _balances[msg.sender] = _totalSupply;
    }

    receive() external payable  {
        buyTokens(msg.sender);
    }
    
    function buyTokens(address beneficiary) public payable {
        require(beneficiary != address(0), "Crowdsale: beneficiary is the zero address");
        
        uint256 weiAmount;
        weiAmount = msg.value;
       
        require(weiAmount != 0, "Crowdsale: weiAmount is 0");
        require(weiAmount >= _min, "Min: sum is too low for the investment");
        
        uint256 tokensAmount = weiAmount * _rate;
        require( tokensAmount >= weiAmount, "SafeMath: multiplication overflow");
        require(tokensAmount <=  _balances[_owner], "SafeMath: subtraction overflow");
        
        uint256 newBalance = _weiRaised + weiAmount;
        require( newBalance >= weiAmount, "SafeMath: sum is overflow");

        
        _balances[_owner]  = _balances[_owner] - tokensAmount;
        _balances[beneficiary] = _balances[beneficiary] + tokensAmount;
        _weiRaised =  newBalance;
 
        emit TokensPurchased(_owner, beneficiary, weiAmount, tokensAmount);
        _wallet.transfer(msg.value);
    }
    
    function transferFrom(address sender, address recipient, uint256 amount) public {
        require(sender != address(0) && sender == msg.sender, "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");
        require(amount <=  _balances[sender], "SafeMath: subtraction overflow");
        uint256 sub = _balances[sender] - amount;
        uint256 sum = _balances[recipient] + amount;
        require(sum >= _balances[recipient], "SafeMath: addition overflow");
        _balances[sender] = sub;
        _balances[recipient] = sum;
        emit Transfer(sender, recipient, amount);
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _owner = newOwner;
        emit OwnershipTransferred(_owner, newOwner);
    }

    function _setMIN(uint value) public {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        require( value > 0 , "Min: the sum cannot be smaller than NULL");
        _min = value;
        emit SetMin(value);
    }
   
}