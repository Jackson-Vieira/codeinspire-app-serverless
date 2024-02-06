import { DynamoDBClient} from "@aws-sdk/client-dynamodb";
import { ScanCommand, DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

async function getTips(event){

    const command = new ScanCommand({
        TableName: process.env.DYNAMODB_TABLE_NAME,
        Select: "ALL_ATTRIBUTES",
    });

    const response = await docClient.send(command);
    const tips = response.Items;

    return {
        statusCode: 200,
        body: JSON.stringify(tips)
    };
};

export const handler = getTips;