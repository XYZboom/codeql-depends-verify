/**
 * @id java-kotlin/extension
 * @name Extension
 * @description Extension
 * @kind problem
 * @problem.severity recommendation
 */

import java

from ExtensionMethod m, RefType t
where m.getExtendedType() = t
select m, m.getQualifiedName() + " " + t.getQualifiedName()