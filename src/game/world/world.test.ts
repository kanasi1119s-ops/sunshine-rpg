import { WORLD_MAPS } from "./world";
import { describeWorldExitIntegrity } from "../map/tile-map-test-helpers";

describeWorldExitIntegrity("世界全体の出入り口の整合性（章をまたぐものを含む）", WORLD_MAPS);
