CREATE TABLE quotes (
    symbol VARCHAR(255),
    marketCenter VARCHAR(255),
    bidQuantity INT,
    askQuantity INT,
    bidPrice DECIMAL(18, 2),
    askPrice DECIMAL(18, 2),
    startTime TIMESTAMP,
    endTime TIMESTAMP,
    quoteConditions VARCHAR(255),
    sipFeed VARCHAR(255),
    sipFeedSeq VARCHAR(255),
    PRIMARY KEY (symbol, startTime, sipFeed, sipFeedSeq)
);

CREATE INDEX idx_quotes_symbol_start_end
ON quotes (symbol, startTime, endTime);