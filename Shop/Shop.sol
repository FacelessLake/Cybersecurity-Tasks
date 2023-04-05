// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract MyShop {

    struct Product{
        string name;
        uint price;
    }
    
    enum Status {Created, Paid}

    struct Order {
        uint id;
        Product product;
        address from;
        address to;
        Status status;
    }

    address owner;
    uint counter;
    Product[5] priceList;
    Order[] payed;
    mapping (address => Order) orders;

    constructor() {
        owner = msg.sender;
        counter = 0;
        priceList[0].name = "product1";
        priceList[0].price = 1000000000000000000;
        priceList[1].name = "product2";
        priceList[1].price = 2000000000000000000;
        priceList[2].name = "product3";
        priceList[2].price = 3000000000000000000;
        priceList[3].name = "product4";
        priceList[3].price = 4000000000000000000;
    }

    function getPriceList() public view returns (string[] memory, uint[] memory) {
        string[] memory names = new string[](priceList.length);
        uint[] memory prices = new uint[](priceList.length);
        for (uint i = 0; i < priceList.length; i++) {
            Product memory product = priceList[i];
            names[i] = product.name;
            prices[i] = product.price;
        }
        return (names, prices);
    }

    function isOrderExists() private view returns (bool) {
        if(orders[msg.sender].id > 0){
            return true;
        } 
        else{
            return false;
        }
    }
    
    function makeOrder(uint chosenProduct) public {
        require(!isOrderExists(), "Please finish current order");
        Order memory newOrder = orderConstuctor(priceList[chosenProduct]);
        orders[msg.sender] = newOrder;
    }

    function deleteOrder() public {
        require(isOrderExists(), "You haven't ordered anything");
        delete(orders[msg.sender]);
    }

    function checkOrder() public view returns (Order memory){
        require(isOrderExists(), "You haven't ordered anything");
        return orders[msg.sender];
    }

    function orderConstuctor(Product memory _prod) private returns(Order memory) {
        counter++;
        Order memory order = Order(
        counter,
        _prod,
        msg.sender,
        address(this),
        Status.Created
        );
        return order;
    }

    function buyChosen() public payable {
        require(isOrderExists(), "You haven't ordered anything");
        uint price = orders[msg.sender].product.price;
        require(msg.value == price, "Please, send corresponding amount of money");
        orders[msg.sender].status = Status.Paid;
        payed.push(orders[msg.sender]);
    }

    function withdrawAll() public {
        require(msg.sender == owner, "You are not allowed to do this");
        address payable _to = payable(owner);
        address _thisContract = address(this);
        _to.transfer(_thisContract.balance);
    }
}