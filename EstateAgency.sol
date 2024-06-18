// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract EstateAgency {

    enum EstateType {
        House,
        Apartments,
        Flat,
        Loft
    }

    enum AdvertisementStatus {
        Opened,
        Closed
    }

    struct Estate {
        string name;
        string addressOfEstate;
        uint estateID;
        EstateType estateType;
        uint rooms;
        string describe;
        address owner;
        bool isActive;
    }

    struct Advertisement {
        address owner;
        address buyer;
        uint price;
        AdvertisementStatus adStatus;
        uint estateID;
        uint dateTime;
        uint adID;
    }

    event EstateCreated(address indexed owner, uint indexed estateID, uint date, EstateType estateType);
    event EstatePurchased(address indexed owner, address indexed buyer, uint indexed adID, uint estateID, AdvertisementStatus adStatus, uint date, uint price);
    event EstateUpdated(address indexed owner, uint indexed estateID, uint date, bool isActive);
    event FundsSent(address indexed receiver, uint amount, uint date);
    event AdCreated(address indexed owner, uint indexed estateID, uint indexed adID, uint date, uint price);
    event AdUpdated(address indexed owner, uint indexed estateID, uint indexed adID, uint date, AdvertisementStatus adStatus);

    Estate[] public estates;
    Advertisement[] public advertisements;
    mapping(address => uint) public balanceSeller;

    modifier enough(uint value, uint price) {
        require(value >= price, unicode"У вас недостаточно средств");
        _;
    }

    modifier isActiveEstate(uint estateID) {
        require(estates[estateID].isActive, unicode"Данная недвижимость недоступна");
        _;
    }

    modifier onlyEstateOwner(uint estateID) {
        require(estates[estateID].owner == msg.sender, unicode"Вы не владелец данной недвижимости");
        _;
    }

    modifier onlyAdOwner(uint adID) {
        require(advertisements[adID].owner == msg.sender, unicode"Вы не владелец данного объявления");
        _;
    }

    modifier isClosedAd(uint adID) {
        require(advertisements[adID].adStatus == AdvertisementStatus.Opened, unicode"Данное объявление закрыто");
        _;
    }

    function createEstate(string memory _name, string memory _addressOfEstate, EstateType _estateType, uint _rooms, string memory _describe) public {
        estates.push(Estate(_name, _addressOfEstate, estates.length, _estateType, _rooms, _describe, msg.sender, true));
        emit EstateCreated(msg.sender, estates.length - 1, block.timestamp, _estateType);
    }

    function createAd(uint estateID, uint _price) public onlyEstateOwner(estateID) isActiveEstate(estateID) {
        advertisements.push(Advertisement(msg.sender, address(0), _price, AdvertisementStatus.Opened, estateID, block.timestamp, advertisements.length));
        emit AdCreated(msg.sender, estateID, advertisements.length - 1, block.timestamp, _price);
    }

    function updateEstateStatus(uint estateID, bool _isActive) public onlyEstateOwner(estateID) {
        estates[estateID].isActive = _isActive;
        emit EstateUpdated(msg.sender, estateID, block.timestamp, _isActive);
    }

    function updateAdStatus(uint adID, AdvertisementStatus _adStatus) public onlyAdOwner(adID) {
        advertisements[adID].adStatus = _adStatus;
        emit AdUpdated(msg.sender, advertisements[adID].estateID, adID, block.timestamp, _adStatus);
    }

    function purchaseEstate(uint adID) public payable isClosedAd(adID) {
        Advertisement memory ad = advertisements[adID];
        balanceSeller[ad.owner] += ad.price;
        ad.buyer = msg.sender;
        ad.adStatus = AdvertisementStatus.Closed;
        advertisements[adID] = ad;
        estates[adID].owner = msg.sender;
        emit EstatePurchased(ad.owner, msg.sender, adID, ad.estateID, AdvertisementStatus.Closed, block.timestamp, ad.price);
        emit FundsSent(ad.owner, ad.price, block.timestamp);
    }

    function withdraw(uint amount) public {
        require(amount <= balanceSeller[msg.sender], unicode"Недостаточный баланс средств");
        payable(msg.sender).transfer(amount);
        balanceSeller[msg.sender] -= amount;
        emit FundsSent(msg.sender, amount, block.timestamp);
    }

    function getEstate(uint estateID) public view returns (Estate memory) {
        return estates[estateID];
    }

    function getAd(uint adID) public view returns (Advertisement memory) {
        return advertisements[adID];
    }

    function getBalance() public view returns (uint) {
        return balanceSeller[msg.sender];
    }

    function getAllEstates() public view returns (Estate[] memory) {
        return estates;
    }

    function getAllAds() public view returns (Advertisement[] memory) {
        return advertisements;
    }
}
